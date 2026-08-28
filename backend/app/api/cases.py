import random
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.db.session import get_db
from app.db.models import Case, Service, Citizen, Department, Jurisdiction, Document, AuditEvent, UserRole
from app.schemas.case import (
    CaseCreateInput, CaseActionInput, DocumentResubmitInput,
    CaseListOut, CaseDetailOut, AvailableActionOut
)
from app.api.deps import get_current_user_context
from app.core.authz import UserContext, ActionEnum, can
from app.core.workflow_engine import WorkflowEngine
from app.core.audit import create_audit_event, GENESIS_HASH

router = APIRouter(prefix="/cases", tags=["Case Management"])

def generate_public_case_id(service_code: str) -> str:
    short_code = service_code.split("_")[0][:3].upper()
    random_num = random.randint(10000, 99999)
    return f"JS-2026-{short_code}-{random_num}"

def compute_citizen_status(state: str) -> str:
    status_map = {
        "DRAFT": "Draft saved. Not submitted.",
        "SUBMITTED": "Application Submitted. Awaiting Initial Verification.",
        "VERIFICATION": "Under Initial Verification with Front-Desk Officer.",
        "DEPARTMENT_REVIEW": "Under Departmental Scrutiny with Revenue Inspector.",
        "ACTION_REQUIRED": "Action Required: Please replace defective document(s).",
        "APPROVAL": "Under Final Review with Competent Authority (Tahsildar).",
        "RESOLVED": "Approved! Official digital certificate is ready.",
        "REJECTED": "Application Rejected. See statutory notes."
    }
    return status_map.get(state, f"In Progress ({state})")

def compute_stage_explanation(state: str, service_title: str = "Service", remarks: Optional[str] = None) -> dict:
    explanations = {
        "DRAFT": {
            "what_happened": "Draft saved locally.",
            "what_it_means": "Your application has been created as a draft.",
            "action_needed": "Complete all questionnaire fields and submit.",
            "what_happens_next": "Once submitted, it will be assigned to a verification desk."
        },
        "SUBMITTED": {
            "what_happened": "Application successfully submitted.",
            "what_it_means": "Your application and uploaded documents have been securely received in the intake queue.",
            "action_needed": "You don't need to do anything right now.",
            "what_happens_next": "A verification officer will check your uploaded documents against statutory rules."
        },
        "VERIFICATION": {
            "what_happened": "Under front-desk document verification.",
            "what_it_means": "The verification officer is checking all uploaded documents for clarity and compliance.",
            "action_needed": "You don't need to do anything right now.",
            "what_happens_next": "Upon successful verification, the application is forwarded for departmental scrutiny."
        },
        "DEPARTMENT_REVIEW": {
            "what_happened": "Under departmental scrutiny.",
            "what_it_means": "The responsible department officer is verifying eligibility and municipal/land records.",
            "action_needed": "You don't need to do anything right now.",
            "what_happens_next": "The reviewing officer will forward recommendations to the competent approving authority."
        },
        "ACTION_REQUIRED": {
            "what_happened": "A document or detail requires correction.",
            "what_it_means": f"The scrutiny desk noted: {remarks or 'Defective or unreadable scan detected.'}",
            "action_needed": "Please upload a clear replacement document using the action box below.",
            "what_happens_next": "Once you submit the replacement, verification will resume automatically."
        },
        "APPROVAL": {
            "what_happened": "Under final statutory approval review.",
            "what_it_means": "The application is with the competent approving authority (Executive Magistrate / Tahsildar).",
            "action_needed": "You don't need to do anything right now.",
            "what_happens_next": "Upon final authorization, your official digital certificate will be generated."
        },
        "RESOLVED": {
            "what_happened": "Application approved & completed.",
            "what_it_means": "Statutory approval has been granted. Your official digital certificate is ready.",
            "action_needed": "You can view and verify your digital certificate below.",
            "what_happens_next": "No further action is required. This case is closed and archived."
        },
        "REJECTED": {
            "what_happened": "Application rejected based on statutory review.",
            "what_it_means": f"The reviewing authority recorded: {remarks or 'Statutory requirements not satisfied.'}",
            "action_needed": "Review the recorded remarks. You may submit a fresh application with valid proofs.",
            "what_happens_next": "Case is closed."
        }
    }
    return explanations.get(state, {
        "what_happened": f"Status: {state}",
        "what_it_means": "Your case is progressing through the authorized workflow.",
        "action_needed": "No action required at this moment.",
        "what_happens_next": "Awaiting next officer action."
    })

@router.post("", response_model=CaseDetailOut, status_code=status.HTTP_201_CREATED)
async def create_case(
    payload: CaseCreateInput,
    current_user: UserContext = Depends(get_current_user_context),
    db: AsyncSession = Depends(get_db)
):
    if not can(current_user, ActionEnum.CREATE_CASE):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only citizens can submit applications."
        )

    # Validate service
    s_stmt = select(Service).where(Service.id == payload.service_id)
    s_res = await db.execute(s_stmt)
    service = s_res.scalar_one_or_none()
    if not service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found.")

    # Validate citizen
    c_stmt = select(Citizen).where(Citizen.id == current_user.citizen_id)
    c_res = await db.execute(c_stmt)
    citizen = c_res.scalar_one_or_none()
    if not citizen:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Citizen profile missing.")

    # Create Case
    public_id = generate_public_case_id(service.code)
    new_case = Case(
        public_case_id=public_id,
        service_id=service.id,
        workflow_version=1,
        citizen_id=citizen.id,
        department_id=service.department_id,
        jurisdiction_id=payload.jurisdiction_id or current_user.jurisdiction_id,
        current_state="SUBMITTED",
        version_id=1,
        form_data_json=payload.form_data,
        submitted_at=datetime.utcnow()
    )
    db.add(new_case)
    await db.flush()

    # Attach uploaded documents if any
    if payload.document_ids:
        for doc_id in payload.document_ids:
            doc_stmt = select(Document).where(Document.id == doc_id)
            doc_res = await db.execute(doc_stmt)
            doc = doc_res.scalar_one_or_none()
            if doc:
                doc.case_id = new_case.id

    # Create Genesis Audit Event
    initial_audit = create_audit_event(
        case_id=new_case.id,
        event_sequence=1,
        actor_id=current_user.user_id,
        actor_role=current_user.role,
        action="SUBMIT",
        from_state="DRAFT",
        to_state="SUBMITTED",
        remarks="Citizen submitted application with attached documents.",
        previous_event_hash=GENESIS_HASH
    )
    db.add(initial_audit)
    await db.commit()

    return await get_case_detail_by_id(new_case.id, current_user, db)

@router.get("", response_model=List[CaseListOut])
async def list_cases(
    status_filter: Optional[str] = None,
    current_user: UserContext = Depends(get_current_user_context),
    db: AsyncSession = Depends(get_db)
):
    stmt = (
        select(Case)
        .options(
            selectinload(Case.service),
            selectinload(Case.citizen)
        )
        .order_by(Case.submitted_at.desc())
    )

    if current_user.role == UserRole.CITIZEN:
        stmt = stmt.where(Case.citizen_id == current_user.citizen_id)
    elif current_user.role in [UserRole.VERIFICATION_OFFICER, UserRole.DEPARTMENT_OFFICER, UserRole.APPROVING_OFFICER]:
        # Enforce Department and Jurisdiction Scoping
        if current_user.department_id:
            stmt = stmt.where(Case.department_id == current_user.department_id)
        if current_user.jurisdiction_id:
            stmt = stmt.where(Case.jurisdiction_id == current_user.jurisdiction_id)

    if status_filter:
        stmt = stmt.where(Case.current_state == status_filter.upper())

    res = await db.execute(stmt)
    cases = res.scalars().all()

    output = []
    for c in cases:
        sla = c.service.sla_days if c.service else 7
        output.append(CaseListOut(
            id=c.id,
            public_case_id=c.public_case_id,
            service_id=c.service_id,
            service_title=c.service.title if c.service else "Service",
            service_code=c.service.code if c.service else "",
            category=c.service.category if c.service else "GENERAL",
            current_state=c.current_state,
            citizen_status=compute_citizen_status(c.current_state),
            citizen_name=c.citizen.full_name if c.citizen else "Citizen",
            version_id=c.version_id,
            sla_days=sla,
            action_required=(c.current_state == "ACTION_REQUIRED"),
            submitted_at=c.submitted_at,
            updated_at=c.updated_at
        ))
    return output

@router.get("/{case_id}", response_model=CaseDetailOut)
async def get_case(
    case_id: str,
    current_user: UserContext = Depends(get_current_user_context),
    db: AsyncSession = Depends(get_db)
):
    return await get_case_detail_by_id(case_id, current_user, db)

async def get_case_detail_by_id(case_id: str, current_user: UserContext, db: AsyncSession) -> CaseDetailOut:
    stmt = (
        select(Case)
        .options(
            selectinload(Case.service),
            selectinload(Case.citizen).selectinload(Citizen.user),
            selectinload(Case.department),
            selectinload(Case.jurisdiction),
            selectinload(Case.documents),
            selectinload(Case.audit_events)
        )
        .where((Case.id == case_id) | (Case.public_case_id == case_id))
    )
    res = await db.execute(stmt)
    c = res.scalar_one_or_none()
    if not c:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Case not found.")

    if not can(current_user, ActionEnum.VIEW_CASE, c):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access Denied: You do not have permission to view this case."
        )

    # Compute available contextual actions
    actions_raw = await WorkflowEngine.get_available_actions_for_user(db, c, current_user)
    available_actions = [AvailableActionOut(**a) for a in actions_raw]

    service_name = c.service.title if c.service else "Service"
    explanation = compute_stage_explanation(c.current_state, service_name, c.resolution_remarks)
    sla = c.service.sla_days if c.service else 7

    return CaseDetailOut(
        id=c.id,
        public_case_id=c.public_case_id,
        service_id=c.service_id,
        service_title=service_name,
        service_code=c.service.code if c.service else "",
        category=c.service.category if c.service else "GENERAL",
        department_id=c.department_id,
        department_name=c.department.name if c.department else "",
        jurisdiction_id=c.jurisdiction_id,
        jurisdiction_name=c.jurisdiction.name if c.jurisdiction else "",
        current_state=c.current_state,
        citizen_status=compute_citizen_status(c.current_state),
        status_explanation=explanation,
        sla_days=sla,
        action_required=(c.current_state == "ACTION_REQUIRED"),
        version_id=c.version_id,
        citizen_name=c.citizen.full_name if c.citizen else "Citizen",
        citizen_aadhaar_last4=c.citizen.synthetic_aadhaar_last4 if c.citizen else "0000",
        citizen_phone=c.citizen.user.phone_number if c.citizen and c.citizen.user else "+91-9876543210",
        form_data=c.form_data_json,
        resolution_remarks=c.resolution_remarks,
        submitted_at=c.submitted_at,
        updated_at=c.updated_at,
        documents=c.documents,
        audit_events=c.audit_events,
        available_actions=available_actions
    )

@router.post("/{case_id}/actions/{action_name}", response_model=CaseDetailOut)
async def execute_case_action(
    case_id: str,
    action_name: str,
    payload: CaseActionInput,
    current_user: UserContext = Depends(get_current_user_context),
    db: AsyncSession = Depends(get_db)
):
    stmt = (
        select(Case)
        .options(
            selectinload(Case.service),
            selectinload(Case.citizen),
            selectinload(Case.department),
            selectinload(Case.jurisdiction),
            selectinload(Case.documents),
            selectinload(Case.audit_events)
        )
        .where((Case.id == case_id) | (Case.public_case_id == case_id))
    )
    res = await db.execute(stmt)
    c = res.scalar_one_or_none()
    if not c:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Case not found.")

    doc_verifs = [dv.model_dump() for dv in payload.document_verifications] if payload.document_verifications else None

    # Execute workflow transition inside database transaction
    await WorkflowEngine.execute_action(
        session=db,
        case=c,
        action_name=action_name.upper(),
        actor=current_user,
        expected_version=payload.version_id,
        remarks=payload.remarks,
        document_verifications=doc_verifs
    )
    await db.commit()

    return await get_case_detail_by_id(c.id, current_user, db)

@router.post("/{case_id}/resubmit-document", response_model=CaseDetailOut)
async def resubmit_deficient_document(
    case_id: str,
    payload: DocumentResubmitInput,
    current_user: UserContext = Depends(get_current_user_context),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Case).options(selectinload(Case.documents), selectinload(Case.citizen)).where(Case.id == case_id)
    res = await db.execute(stmt)
    c = res.scalar_one_or_none()
    if not c:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Case not found.")

    if not can(current_user, ActionEnum.RESUBMIT_DOCUMENTS, c):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized to resubmit documents.")

    # Update the target document to REPLACED and attach new doc
    target_doc = next((d for d in c.documents if d.id == payload.target_document_id), None)
    if target_doc:
        target_doc.status = "REPLACED"

    replacement_doc_stmt = select(Document).where(Document.id == payload.replacement_document_id)
    rep_res = await db.execute(replacement_doc_stmt)
    rep_doc = rep_res.scalar_one_or_none()
    if rep_doc:
        rep_doc.case_id = c.id
        rep_doc.requirement_id = target_doc.requirement_id if target_doc else rep_doc.requirement_id
        rep_doc.status = "AVAILABLE"
        rep_doc.version = (target_doc.version + 1) if target_doc else 2

    # Execute RESUBMIT_DOCUMENTS workflow action
    await WorkflowEngine.execute_action(
        session=db,
        case=c,
        action_name="RESUBMIT_DOCUMENTS",
        actor=current_user,
        expected_version=payload.version_id,
        remarks=payload.remarks
    )
    await db.commit()

    return await get_case_detail_by_id(c.id, current_user, db)
