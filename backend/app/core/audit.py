import hashlib
from datetime import datetime
from typing import Optional
from app.db.models import AuditEvent

GENESIS_HASH = "0000000000000000000000000000000000000000000000000000000000000000"

def calculate_event_hash(
    previous_event_hash: str,
    case_id: str,
    event_sequence: int,
    actor_id: str,
    actor_role: str,
    action: str,
    from_state: str,
    to_state: str,
    timestamp: datetime,
    remarks: Optional[str] = ""
) -> str:
    raw_str = f"{previous_event_hash}:{case_id}:{event_sequence}:{actor_id}:{actor_role}:{action}:{from_state}:{to_state}:{timestamp.isoformat()}:{remarks or ''}"
    return hashlib.sha256(raw_str.encode("utf-8")).hexdigest()

def create_audit_event(
    case_id: str,
    event_sequence: int,
    actor_id: str,
    actor_role: str,
    action: str,
    from_state: str,
    to_state: str,
    remarks: Optional[str] = "",
    previous_event_hash: Optional[str] = None
) -> AuditEvent:
    now = datetime.utcnow()
    prev_hash = previous_event_hash or GENESIS_HASH
    event_hash = calculate_event_hash(
        previous_event_hash=prev_hash,
        case_id=case_id,
        event_sequence=event_sequence,
        actor_id=actor_id,
        actor_role=actor_role,
        action=action,
        from_state=from_state,
        to_state=to_state,
        timestamp=now,
        remarks=remarks
    )
    
    return AuditEvent(
        case_id=case_id,
        event_sequence=event_sequence,
        actor_id=actor_id,
        actor_role=actor_role,
        action=action,
        from_state=from_state,
        to_state=to_state,
        remarks=remarks,
        previous_event_hash=prev_hash,
        event_hash=event_hash,
        created_at=now
    )

def verify_audit_chain(events: list[AuditEvent]) -> bool:
    """Verifies that an entire chain of audit events is cryptographically unbroken."""
    if not events:
        return True
    
    expected_prev = GENESIS_HASH
    for ev in events:
        if ev.previous_event_hash != expected_prev:
            return False
        
        computed_hash = calculate_event_hash(
            previous_event_hash=ev.previous_event_hash,
            case_id=ev.case_id,
            event_sequence=ev.event_sequence,
            actor_id=ev.actor_id,
            actor_role=ev.actor_role,
            action=ev.action,
            from_state=ev.from_state,
            to_state=ev.to_state,
            timestamp=ev.created_at,
            remarks=ev.remarks
        )
        if computed_hash != ev.event_hash:
            return False
        
        expected_prev = ev.event_hash
        
    return True
