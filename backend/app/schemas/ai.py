from pydantic import BaseModel
from typing import Optional, Dict, Any

class AIQueryInput(BaseModel):
    prompt: str
    session_context: Optional[Dict[str, Any]] = None

class AIQueryOutput(BaseModel):
    recommended_service_id: Optional[str] = None
    service_title: Optional[str] = None
    explanation: str
    confidence_score: float
