from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.db.models import NotificationOutbox

class NotificationService:
    @staticmethod
    async def process_pending_outbox(session: AsyncSession) -> int:
        stmt = select(NotificationOutbox).where(NotificationOutbox.status == "PENDING")
        res = await session.execute(stmt)
        pending_records = res.scalars().all()
        
        count = 0
        for item in pending_records:
            # Synthetic delivery simulation (In-app, SMS mock, Email mock)
            item.status = "PROCESSED"
            item.processed_at = datetime.utcnow()
            count += 1
            
        await session.flush()
        return count
