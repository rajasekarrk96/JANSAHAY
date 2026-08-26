from typing import List, Dict, Any, Optional
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models import Case, WorkflowDefinition, AuditEvent, NotificationOutbox, Document, Citizen
from app.core.authz import UserContext, ActionEnum, can
from app.core.audit import create_audit_event, GENESIS_HASH

class WorkflowEngine:
    @staticmethod
    async def get_workflow_definition(session: AsyncSession, service_id: str, version: int = 1) -> Dict[str, Any]:
        stmt = select(WorkflowDefinition).where(
            WorkflowDefinition.service_id == service_id,
            WorkflowDefinition.version == version,
            WorkflowDefinition.is_active == True
        )
        result = await session.execute(stmt)
        wf = result.scalar_one_or_none()
        if not wf:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Workflow definition not found for service_id={service_id}, version={version}"
            )
        return wf.definition_json

    @staticmethod
    def get_allowed_transitions(definition: Dict[str, Any], current_state: str) -> List[Dict[str, Any]]:
        transitions = definition.get("transitions", [])
        allowed = []
        for t in transitions:
            from_state = t.get("from_state")
            if isinstance(from_state, list):
                if current_state in from_state:
                    allowed.append(t)
            elif from_state == current_state:
                allowed.append(t)
        return allowed

    @staticmethod
    async def get_available_actions_for_user(
        session: AsyncSession,
        case: Case,
        actor: UserContext
    ) -> List[Dict[str, Any]]:
        definition = await WorkflowEngine.get_workflow_definition(session, case.service_id, case.workflow_version)
        possible_transitions = WorkflowEngine.get_allowed_transitions(definition, case.current_state)
        
        available = []
        for t in possible_transitions:
            action_name = t.get("action")
            # Check role in definition
            allowed_roles = t.get("allowed_roles", [])
            if actor.role in allowed_roles:
                # Check contextual authz can()
                try:
                    action_enum = ActionEnum(action_name)
                    if can(actor, action_enum, case):
                        available.append({
                            "action": action_name,
                            "to_state": t.get("to_state"),
                            "citizen_status": t.get("citizen_status"),
                            "requires_remarks": t.get("requires_remarks", False),
                            "label": action_name.replace("_", " ").title()
                        })
                except ValueError:
                    # Action name might not be in ActionEnum or custom
                    pass
        return available

    @staticmethod
    async def execute_action(
        session: AsyncSession,
        case: Case,
        action_name: str,
        actor: UserContext,
        expected_version: int,
        remarks: Optional[str] = None,
        document_verifications: Optional[List[Dict[str, str]]] = None
    ) -> Case:
        # 1. Optimistic Locking check
        if case.version_id != expected_version:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Conflict: Case version mismatch. Provided={expected_version}, Active={case.version_id}. Refresh the case view."
            )

        # 2. Check Contextual Authorization
        try:
            action_enum = ActionEnum(action_name)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unknown workflow action: {action_name}"
            )

        if not can(actor, action_enum, case):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Actor role {actor.role} is not authorized to execute {action_name} on this case."
            )

        # 3. Load Workflow Definition
        definition = await WorkflowEngine.get_workflow_definition(session, case.service_id, case.workflow_version)
        possible_transitions = WorkflowEngine.get_allowed_transitions(definition, case.current_state)
        
        matched_transition = None
        for t in possible_transitions:
            if t.get("action") == action_name and actor.role in t.get("allowed_roles", []):
                matched_transition = t
                break

        if not matched_transition:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Action '{action_name}' is not a valid transition from state '{case.current_state}' for role '{actor.role}'."
            )

        from_state = case.current_state
        to_state = matched_transition.get("to_state")
        guards = matched_transition.get("guards", [])

        # 4. Handle Document Verifications if provided (e.g. during VERIFY or REQUEST_CORRECTION)
        if document_verifications:
            # Query existing documents
            stmt = select(Document).where(Document.case_id == case.id)
            res = await session.execute(stmt)
            case_docs = {d.id: d for d in res.scalars().all()}

            for dv in document_verifications:
                doc_id = dv.get("document_id")
                new_doc_status = dv.get("status")
                doc_notes = dv.get("notes")
                if doc_id in case_docs and new_doc_status:
                    case_docs[doc_id].status = new_doc_status
                    if doc_notes:
                        case_docs[doc_id].verification_notes = doc_notes

        # 5. Evaluate Guards
        if "ALL_MANDATORY_DOCS_VERIFIED" in guards:
            stmt = select(Document).where(Document.case_id == case.id)
            res = await session.execute(stmt)
            docs = res.scalars().all()
            unverified = [d.file_name for d in docs if d.status not in ["VERIFIED", "AVAILABLE"]]
            if unverified:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Cannot execute {action_name}: Unverified documents: {', '.join(unverified)}"
                )

        if "ALL_DEFICIENT_DOCS_REPLACED" in guards:
            stmt = select(Document).where(Document.case_id == case.id)
            res = await session.execute(stmt)
            docs = res.scalars().all()
            still_deficient = [d.file_name for d in docs if d.status == "REPLACEMENT_REQUIRED"]
            if still_deficient:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Deficient documents remaining: {', '.join(still_deficient)}"
                )

        # 6. Fetch previous audit hash
        audit_stmt = select(AuditEvent).where(AuditEvent.case_id == case.id).order_by(AuditEvent.event_sequence.desc())
        audit_res = await session.execute(audit_stmt)
        last_audit = audit_res.scalars().first()
        prev_hash = last_audit.event_hash if last_audit else GENESIS_HASH
        next_seq = (last_audit.event_sequence + 1) if last_audit else 1

        # 7. Create Audit Event
        audit_event = create_audit_event(
            case_id=case.id,
            event_sequence=next_seq,
            actor_id=actor.user_id,
            actor_role=actor.role,
            action=action_name,
            from_state=from_state,
            to_state=to_state,
            remarks=remarks,
            previous_event_hash=prev_hash
        )
        session.add(audit_event)

        # 8. Create Notification Outbox entry for Citizen
        cit_stmt = select(Citizen.user_id).where(Citizen.id == case.citizen_id)
        cit_res = await session.execute(cit_stmt)
        recipient_id = cit_res.scalar_one_or_none() or actor.user_id
        
        citizen_message = matched_transition.get("citizen_status", f"Case moved to {to_state}")
        if remarks:
            citizen_message += f" | Officer Remarks: {remarks}"

        notification = NotificationOutbox(
            case_id=case.id,
            recipient_user_id=recipient_id,
            channel="IN_APP",
            title=f"Update on Case {case.public_case_id}",
            message=citizen_message,
            status="PENDING"
        )
        session.add(notification)

        # 9. Update Case State & Version
        case.current_state = to_state
        case.version_id += 1
        if remarks:
            case.resolution_remarks = remarks

        await session.flush()
        return case
