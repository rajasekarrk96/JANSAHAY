from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.ai import AIQueryInput, AIQueryOutput
from app.core.ai_service import AIService
from app.api.deps import get_current_user_context
from app.core.authz import UserContext

router = APIRouter(prefix="/ai", tags=["Assistive AI"])

@router.post("/assist", response_model=AIQueryOutput)
async def get_ai_assistance(
    payload: AIQueryInput,
    db: AsyncSession = Depends(get_db)
):
    result = await AIService.get_assistive_guidance(
        prompt=payload.prompt,
        session_context=payload.session_context
    )
    return AIQueryOutput(**result)
