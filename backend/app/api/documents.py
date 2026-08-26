import os
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.db.session import get_db
from app.db.models import Document, Case, ServiceRequirement
from app.schemas.document import DocumentOut
from app.api.deps import get_current_user_context
from app.core.authz import UserContext, ActionEnum, can
from app.core.document_service import DocumentService

router = APIRouter(prefix="/documents", tags=["Document Management"])

@router.post("/upload", response_model=DocumentOut, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    requirement_id: str = Form(...),
    case_id: str = Form(default="temp"),
    current_user: UserContext = Depends(get_current_user_context),
    db: AsyncSession = Depends(get_db)
):
    # Process & quarantine file
    doc_info = await DocumentService.process_and_quarantine_upload(file, case_id=case_id)
    
    # Save metadata record
    new_doc = Document(
        case_id=case_id if case_id != "temp" else "",
        requirement_id=requirement_id,
        file_name=doc_info["file_name"],
        file_path=doc_info["file_path"],
        mime_type=doc_info["mime_type"],
        file_size_bytes=doc_info["file_size_bytes"],
        status=doc_info["status"],
        version=1
    )
    db.add(new_doc)
    await db.commit()
    await db.refresh(new_doc)
    return new_doc

@router.get("/{document_id}/download")
async def download_document(
    document_id: str,
    current_user: UserContext = Depends(get_current_user_context),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Document).options(selectinload(Document.case)).where(Document.id == document_id)
    res = await db.execute(stmt)
    doc = res.scalar_one_or_none()
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found.")

    # Contextual authz check
    if doc.case and not can(current_user, ActionEnum.VIEW_DOCUMENT, doc):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied to this document.")

    if not os.path.exists(doc.file_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Physical file missing from storage.")

    return FileResponse(
        path=doc.file_path,
        filename=doc.file_name,
        media_type=doc.mime_type
    )
