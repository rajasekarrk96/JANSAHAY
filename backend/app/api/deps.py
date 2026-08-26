from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.db.models import User, Citizen, Officer, Department, Jurisdiction
from app.core.security import decode_access_token
from app.core.authz import UserContext

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)

async def get_current_user_context(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> UserContext:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated. Bearer token required.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = payload["sub"]
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive."
        )

    citizen_id = None
    officer_id = None
    department_id = None
    jurisdiction_id = None

    if user.role == "CITIZEN":
        c_stmt = select(Citizen).where(Citizen.user_id == user.id)
        c_res = await db.execute(c_stmt)
        citizen = c_res.scalar_one_or_none()
        if citizen:
            citizen_id = citizen.id
            # Also associate citizen's home jurisdiction
            j_stmt = select(Jurisdiction).where(Jurisdiction.code == "DELHI_CENTRAL")
            j_res = await db.execute(j_stmt)
            jur = j_res.scalar_one_or_none()
            if jur:
                jurisdiction_id = jur.id
    elif user.role in ["VERIFICATION_OFFICER", "DEPARTMENT_OFFICER", "APPROVING_OFFICER"]:
        o_stmt = select(Officer).where(Officer.user_id == user.id)
        o_res = await db.execute(o_stmt)
        officer = o_res.scalar_one_or_none()
        if officer:
            officer_id = officer.id
            department_id = officer.department_id
            jurisdiction_id = officer.jurisdiction_id

    return UserContext(
        user_id=user.id,
        username=user.username,
        role=user.role,
        citizen_id=citizen_id,
        officer_id=officer_id,
        department_id=department_id,
        jurisdiction_id=jurisdiction_id
    )
