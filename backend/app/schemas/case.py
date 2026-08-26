from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from app.schemas.document import DocumentOut, DocumentVerificationInput

class AuditEventOut(BaseModel):
    id: str
    event_sequence: int
    actor_id: str
    actor_role: str
    action: str
    from_state: str
    to_state: str
    remarks: Optional[str] = None
    previous_event_hash: str
    event_hash: str
    created_at: datetime

    class Config:
        from_attributes = True

class AvailableActionOut(BaseModel):
    action: str
    to_state: str
    citizen_status: Optional[str] = None
    requires_remarks: bool = False
    label: str

class CaseCreateInput(BaseModel):
    service_id: str
    jurisdiction_id: str
    form_data: Dict[str, Any]
    document_ids: List[str] = []

class CaseActionInput(BaseModel):
    version_id: int
    remarks: Optional[str] = None
    document_verifications: Optional[List[DocumentVerificationInput]] = None

class DocumentResubmitInput(BaseModel):
    version_id: int
    replacement_document_id: str
    target_document_id: str
    remarks: Optional[str] = "Citizen replaced defective document"

class CaseListOut(BaseModel):
    id: str
    public_case_id: str
    service_id: str
    service_title: str
    service_code: str
    category: str
    current_state: str
    citizen_status: str
    citizen_name: str
    version_id: int
    action_required: bool = False
    submitted_at: datetime
    updated_at: datetime

class CaseDetailOut(BaseModel):
    id: str
    public_case_id: str
    service_id: str
    service_title: str
    service_code: str
    category: str
    department_id: str
    department_name: str
    jurisdiction_id: str
    jurisdiction_name: str
    current_state: str
    citizen_status: str
    action_required: bool = False
    version_id: int
    citizen_name: str
    citizen_aadhaar_last4: str
    citizen_phone: str
    form_data: Dict[str, Any]
    resolution_remarks: Optional[str] = None
    submitted_at: datetime
    updated_at: datetime
    documents: List[DocumentOut] = []
    audit_events: List[AuditEventOut] = []
    available_actions: List[AvailableActionOut] = []
