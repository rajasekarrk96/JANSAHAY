from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.db.models import AuditEvent, Case
from app.core.audit import verify_audit_chain
from app.db.init_db import init_db_data

router = APIRouter(prefix="/admin", tags=["Administration & Demo Control"])

@router.post("/reset-demo")
async def reset_demo_database(db: AsyncSession = Depends(get_db)):
    """Restores all tables to pristine initial seed state."""
    await init_db_data(db)
    return {
        "status": "SUCCESS",
        "message": "JANSAHAY demo database successfully reset to pristine seed state."
    }

@router.get("/verify-audit-chain/{case_id}")
async def check_case_audit_integrity(case_id: str, db: AsyncSession = Depends(get_db)):
    c_stmt = select(Case).where((Case.id == case_id) | (Case.public_case_id == case_id))
    c_res = await db.execute(c_stmt)
    c = c_res.scalar_one_or_none()
    target_id = c.id if c else case_id

    stmt = select(AuditEvent).where(AuditEvent.case_id == target_id).order_by(AuditEvent.event_sequence.asc())
    res = await db.execute(stmt)
    events = res.scalars().all()
    
    if not events:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No audit events found for this case.")

    is_valid = verify_audit_chain(events)
    return {
        "case_id": case_id,
        "event_count": len(events),
        "is_chain_unbroken": is_valid,
        "genesis_hash": events[0].previous_event_hash,
        "latest_hash": events[-1].event_hash,
        "events": [
            {
                "sequence": e.event_sequence,
                "action": e.action,
                "actor_role": e.actor_role,
                "from_state": e.from_state,
                "to_state": e.to_state,
                "previous_event_hash": e.previous_event_hash,
                "event_hash": e.event_hash,
                "created_at": e.created_at
            }
            for e in events
        ]
    }
