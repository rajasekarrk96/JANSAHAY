from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List, Optional
from app.db.session import get_db
from app.db.models import Service, ServiceRequirement
from app.schemas.service import ServiceOut

router = APIRouter(prefix="/services", tags=["Public Services"])

@router.get("", response_model=List[ServiceOut])
async def list_services(category: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    stmt = select(Service).options(selectinload(Service.requirements)).where(Service.is_active == True)
    if category:
        stmt = stmt.where(Service.category == category.upper())
    result = await db.execute(stmt)
    services = result.scalars().all()
    return services

@router.get("/{service_id}", response_model=ServiceOut)
async def get_service(service_id: str, db: AsyncSession = Depends(get_db)):
    stmt = select(Service).options(selectinload(Service.requirements)).where(
        (Service.id == service_id) | (Service.code == service_id)
    )
    result = await db.execute(stmt)
    service = result.scalar_one_or_none()
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )
    return service
