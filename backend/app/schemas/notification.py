from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class NotificationOut(BaseModel):
    id: str
    case_id: str
    channel: str
    title: str
    message: str
    status: str
    created_at: datetime
    processed_at: Optional[datetime] = None

    class Config:
        from_attributes = True
