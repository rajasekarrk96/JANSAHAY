from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.db.models import User, Citizen, Officer, Department, Jurisdiction
from app.core.security import verify_password, create_access_token
from app.schemas.auth import LoginRequest, TokenResponse, UserProfile
from app.api.deps import get_current_user_context
from app.core.authz import UserContext

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)):
    stmt = select(User).where(User.username == payload.username)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password."
        )

    profile_id = None
    full_name = user.username
    dept_id = None
    dept_code = None
    jur_id = None
    jur_code = None
    designation = None

    if user.role == "CITIZEN":
        c_stmt = select(Citizen).where(Citizen.user_id == user.id)
        c_res = await db.execute(c_stmt)
        citizen = c_res.scalar_one_or_none()
        if citizen:
            profile_id = citizen.id
            full_name = citizen.full_name
    else:
        o_stmt = select(Officer).where(Officer.user_id == user.id)
        o_res = await db.execute(o_stmt)
        officer = o_res.scalar_one_or_none()
        if officer:
            profile_id = officer.id
            full_name = officer.full_name
            dept_id = officer.department_id
            jur_id = officer.jurisdiction_id
            designation = officer.designation

            # Get codes
            d_stmt = select(Department).where(Department.id == dept_id)
            d_res = await db.execute(d_stmt)
            dept = d_res.scalar_one_or_none()
            if dept:
                dept_code = dept.code

            j_stmt = select(Jurisdiction).where(Jurisdiction.id == jur_id)
            j_res = await db.execute(j_stmt)
            jur = j_res.scalar_one_or_none()
            if jur:
                jur_code = jur.code

    token = create_access_token(
        subject=user.id,
        extra_claims={
            "role": user.role,
            "username": user.username,
            "department_id": dept_id,
            "jurisdiction_id": jur_id
        }
    )

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=UserProfile(
            id=user.id,
            username=user.username,
            email=user.email,
            role=user.role,
            full_name=full_name,
            profile_id=profile_id,
            department_id=dept_id,
            department_code=dept_code,
            jurisdiction_id=jur_id,
            jurisdiction_code=jur_code,
            designation=designation
        )
    )

@router.get("/me", response_model=UserProfile)
async def get_me(
    current_user: UserContext = Depends(get_current_user_context),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(User).where(User.id == current_user.user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    full_name = user.username
    profile_id = current_user.citizen_id or current_user.officer_id
    dept_code = None
    jur_code = None
    designation = None

    if current_user.role == "CITIZEN":
        c_stmt = select(Citizen).where(Citizen.id == current_user.citizen_id)
        c_res = await db.execute(c_stmt)
        citizen = c_res.scalar_one_or_none()
        if citizen:
            full_name = citizen.full_name
    elif current_user.officer_id:
        o_stmt = select(Officer).where(Officer.id == current_user.officer_id)
        o_res = await db.execute(o_stmt)
        officer = o_res.scalar_one_or_none()
        if officer:
            full_name = officer.full_name
            designation = officer.designation

            if officer.department_id:
                d_stmt = select(Department).where(Department.id == officer.department_id)
                d_res = await db.execute(d_stmt)
                dept = d_res.scalar_one_or_none()
                if dept:
                    dept_code = dept.code

            if officer.jurisdiction_id:
                j_stmt = select(Jurisdiction).where(Jurisdiction.id == officer.jurisdiction_id)
                j_res = await db.execute(j_stmt)
                jur = j_res.scalar_one_or_none()
                if jur:
                    jur_code = jur.code

    return UserProfile(
        id=user.id,
        username=user.username,
        email=user.email,
        role=user.role,
        full_name=full_name,
        profile_id=profile_id,
        department_id=current_user.department_id,
        department_code=dept_code,
        jurisdiction_id=current_user.jurisdiction_id,
        jurisdiction_code=jur_code,
        designation=designation
    )

@router.get("/demo-users")
async def get_demo_personas(db: AsyncSession = Depends(get_db)):
    """Returns curated synthetic personas for easy 1-click demo switcher."""
    return [
        {
            "username": "citizen_rahul",
            "password": "Password123!",
            "role": "CITIZEN",
            "full_name": "Rahul Sharma (Citizen)",
            "description": "Citizen in Central Delhi applying for Income Certificate & EPFO claim"
        },
        {
            "username": "vo_delhi_rev",
            "password": "Password123!",
            "role": "VERIFICATION_OFFICER",
            "full_name": "Sunil Verma (Verification Officer)",
            "description": "Front-desk revenue officer validating identity & initial documents"
        },
        {
            "username": "do_delhi_rev",
            "password": "Password123!",
            "role": "DEPARTMENT_OFFICER",
            "full_name": "Priya Nair (Department Officer)",
            "description": "Desk scrutiny officer inspecting revenue records and forwarding cases"
        },
        {
            "username": "ao_delhi_rev",
            "password": "Password123!",
            "role": "APPROVING_OFFICER",
            "full_name": "Rajesh Kumar (Tehsildar / Approver)",
            "description": "Competent statutory authority granting final certificate approval"
        },
        {
            "username": "vo_epfo_delhi",
            "password": "Password123!",
            "role": "VERIFICATION_OFFICER",
            "full_name": "Amit Roy (EPFO Verifier)",
            "description": "EPFO desk officer verifying establishment UAN claims"
        },
        {
            "username": "do_grievance_delhi",
            "password": "Password123!",
            "role": "DEPARTMENT_OFFICER",
            "full_name": "Sanjay Gupta (Grievance Nodal Officer)",
            "description": "Public grievance redressal officer resolving civic complaints"
        }
    ]
