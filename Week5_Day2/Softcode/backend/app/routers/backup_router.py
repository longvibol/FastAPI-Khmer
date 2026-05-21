from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from app.models.user import User
from app.core.deps import get_current_admin

router = APIRouter(prefix="/api/backup", tags=["Backup"])


@router.get("/download")
def download_backup(admin: User = Depends(get_current_admin)):
    db_file = Path(__file__).resolve().parent.parent / "file.db"
    if not db_file.exists():
        raise HTTPException(status_code=404, detail="SQLite file.db not found. You are probably using PostgreSQL.")
    return FileResponse(str(db_file), filename="file.db", media_type="application/octet-stream")
