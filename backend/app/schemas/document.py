from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class DocumentOut(BaseModel):
    id: str
    case_id: str
    requirement_id: str
    file_name: str
    mime_type: str
    file_size_bytes: int
    status: str
    version: int
    verification_notes: Optional[str] = None
    uploaded_at: datetime

    class Config:
        from_attributes = True

class DocumentVerificationInput(BaseModel):
    document_id: str
    status: str # VERIFIED, REPLACEMENT_REQUIRED
    notes: Optional[str] = None
