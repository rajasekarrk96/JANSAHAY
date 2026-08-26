from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class ServiceRequirementOut(BaseModel):
    id: str
    document_type_code: str
    document_name: str
    is_mandatory: bool
    allowed_extensions: str
    max_size_kb: int

    class Config:
        from_attributes = True

class ServiceOut(BaseModel):
    id: str
    code: str
    title: str
    category: str
    department_id: str
    sla_days: int
    eligibility_criteria_json: Dict[str, Any]
    requirements: List[ServiceRequirementOut] = []

    class Config:
        from_attributes = True
