from pydantic import BaseModel, EmailStr
from typing import Optional

class LoginRequest(BaseModel):
    username: str
    password: str

class UserProfile(BaseModel):
    id: str
    username: str
    email: str
    role: str
    full_name: str
    profile_id: Optional[str] = None
    department_id: Optional[str] = None
    department_code: Optional[str] = None
    jurisdiction_id: Optional[str] = None
    jurisdiction_code: Optional[str] = None
    designation: Optional[str] = None

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserProfile
