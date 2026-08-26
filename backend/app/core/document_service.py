import os
import aiofiles
from fastapi import UploadFile, HTTPException, status
from app.config import settings

ALLOWED_MIME_TYPES = {
    "application/pdf": ".pdf",
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/jpg": ".jpg"
}
MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024 # 5 MB

class DocumentService:
    @staticmethod
    def ensure_storage_dir(case_id: str = "temp") -> str:
        target_dir = os.path.join(settings.STORAGE_PATH, case_id)
        os.makedirs(target_dir, exist_ok=True)
        return target_dir

    @staticmethod
    async def process_and_quarantine_upload(file: UploadFile, case_id: str = "temp") -> dict:
        content_type = file.content_type
        if content_type not in ALLOWED_MIME_TYPES:
            # Fallback check extension
            ext = os.path.splitext(file.filename)[1].lower()
            if ext not in [".pdf", ".jpg", ".jpeg", ".png"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid file type. Supported formats: PDF, JPG, PNG. Received: {content_type or ext}"
                )

        target_dir = DocumentService.ensure_storage_dir(case_id)
        import uuid
        file_uuid = str(uuid.uuid4())
        ext = ALLOWED_MIME_TYPES.get(content_type, os.path.splitext(file.filename)[1].lower())
        saved_filename = f"{file_uuid}{ext}"
        saved_path = os.path.join(target_dir, saved_filename)

        total_size = 0
        async with aiofiles.open(saved_path, "wb") as out_file:
            while chunk := await file.read(1024 * 64):
                total_size += len(chunk)
                if total_size > MAX_FILE_SIZE_BYTES:
                    os.remove(saved_path)
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="File exceeds maximum allowed size of 5MB."
                    )
                await out_file.write(chunk)

        # Synthetic malware / antivirus check
        scan_passed = True # All synthetic demo files pass
        final_status = "AVAILABLE" if scan_passed else "SCAN_FAILED"

        return {
            "file_name": file.filename,
            "file_path": saved_path,
            "mime_type": content_type or "application/octet-stream",
            "file_size_bytes": total_size,
            "status": final_status
        }
