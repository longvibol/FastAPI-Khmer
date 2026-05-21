from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}


async def save_upload_file(upload_file: UploadFile, folder: str) -> str:
    if not upload_file or not upload_file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")

    ext = Path(upload_file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Only image files are allowed")

    upload_dir = Path(folder)
    upload_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{uuid4().hex}{ext}"
    file_path = upload_dir / filename

    content = await upload_file.read()
    file_path.write_bytes(content)

    # Convert app/uploads/... to /uploads/... for browser access
    return "/" + str(file_path).replace("app/", "").replace("\\", "/")
