from enum import Enum
from typing import Optional, Any
from pydantic import BaseModel
from app.db.models import UserRole, Case, Document

class ActionEnum(str, Enum):
    VIEW_CASE = "VIEW_CASE"
    CREATE_CASE = "CREATE_CASE"
    VERIFY = "VERIFY"
    REQUEST_CORRECTION = "REQUEST_CORRECTION"
    FORWARD = "FORWARD"
    APPROVE = "APPROVE"
    REJECT = "REJECT"
    RESUBMIT_DOCUMENTS = "RESUBMIT_DOCUMENTS"
    VIEW_DOCUMENT = "VIEW_DOCUMENT"
    RESET_DEMO = "RESET_DEMO"
    VIEW_AUDIT = "VIEW_AUDIT"

class UserContext(BaseModel):
    user_id: str
    username: str
    role: str
    citizen_id: Optional[str] = None
    officer_id: Optional[str] = None
    department_id: Optional[str] = None
    jurisdiction_id: Optional[str] = None

# Base permissions by role
ROLE_ACTION_PERMISSIONS = {
    UserRole.CITIZEN: {
        ActionEnum.VIEW_CASE,
        ActionEnum.CREATE_CASE,
        ActionEnum.RESUBMIT_DOCUMENTS,
        ActionEnum.VIEW_DOCUMENT,
        ActionEnum.VIEW_AUDIT
    },
    UserRole.VERIFICATION_OFFICER: {
        ActionEnum.VIEW_CASE,
        ActionEnum.VERIFY,
        ActionEnum.REQUEST_CORRECTION,
        ActionEnum.REJECT,
        ActionEnum.VIEW_DOCUMENT,
        ActionEnum.VIEW_AUDIT
    },
    UserRole.DEPARTMENT_OFFICER: {
        ActionEnum.VIEW_CASE,
        ActionEnum.FORWARD,
        ActionEnum.REQUEST_CORRECTION,
        ActionEnum.REJECT,
        ActionEnum.VIEW_DOCUMENT,
        ActionEnum.VIEW_AUDIT
    },
    UserRole.APPROVING_OFFICER: {
        ActionEnum.VIEW_CASE,
        ActionEnum.APPROVE,
        ActionEnum.REJECT,
        ActionEnum.VIEW_DOCUMENT,
        ActionEnum.VIEW_AUDIT
    },
    UserRole.SYSTEM_ADMIN: {
        ActionEnum.VIEW_CASE,
        ActionEnum.VIEW_DOCUMENT,
        ActionEnum.VIEW_AUDIT,
        ActionEnum.RESET_DEMO
    }
}

def can(actor: UserContext, action: ActionEnum, resource: Optional[Any] = None) -> bool:
    """
    Evaluates whether the given actor is authorized to perform the requested action
    on the target resource (Case, Document, or None).
    Enforces role capability, department isolation, jurisdiction isolation, and citizen ownership.
    Defaults to DENY (False).
    """
    if not actor:
        return False

    # Check if role has baseline action permission
    allowed_actions = ROLE_ACTION_PERMISSIONS.get(actor.role, set())
    if action not in allowed_actions:
        return False

    # If action is generic without specific resource (e.g. CREATE_CASE, RESET_DEMO)
    if resource is None:
        if action == ActionEnum.CREATE_CASE and actor.role == UserRole.CITIZEN:
            return True
        if action == ActionEnum.RESET_DEMO:
            return True # In demo mode allow demo reset
        return True

    # Resource is a Case
    if isinstance(resource, Case):
        # 1. Citizen authorization: Case must belong to the citizen
        if actor.role == UserRole.CITIZEN:
            return actor.citizen_id is not None and resource.citizen_id == actor.citizen_id

        # 2. Officer authorization: Must match department AND jurisdiction
        if actor.role in [UserRole.VERIFICATION_OFFICER, UserRole.DEPARTMENT_OFFICER, UserRole.APPROVING_OFFICER]:
            if not actor.department_id or resource.department_id != actor.department_id:
                return False
            if not actor.jurisdiction_id or resource.jurisdiction_id != actor.jurisdiction_id:
                return False
            return True

        # 3. System Admin: Read-only inspection
        if actor.role == UserRole.SYSTEM_ADMIN:
            return action in [ActionEnum.VIEW_CASE, ActionEnum.VIEW_AUDIT]

    # Resource is a Document
    if isinstance(resource, Document):
        if resource.case is None:
            return True
        # Delegate to case permissions
        return can(actor, ActionEnum.VIEW_CASE, resource.case)

    return False
