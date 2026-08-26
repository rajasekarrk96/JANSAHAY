from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.db.session import get_db
from app.db.models import NotificationOutbox
from app.schemas.notification import NotificationOut
from app.api.deps import get_current_user_context
from app.core.authz import UserContext
from app.core.notification_service import NotificationService

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("", response_model=List[NotificationOut])
async def list_user_notifications(
    current_user: UserContext = Depends(get_current_user_context),
    db: AsyncSession = Depends(get_db)
):
    stmt = (
        select(NotificationOutbox)
        .where(NotificationOutbox.recipient_user_id == current_user.user_id)
        .order_by(NotificationOutbox.created_at.desc())
    )
    res = await db.execute(stmt)
    return res.scalars().all()

@router.post("/sweep")
async def sweep_notifications(db: AsyncSession = Depends(get_db)):
    processed_count = await NotificationService.process_pending_outbox(db)
    await db.commit()
    return {"processed": processed_count}
