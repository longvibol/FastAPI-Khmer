from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

router = APIRouter(prefix="/api/backup", tags=["Backup"])


@router.get("/download")
def download_database_backup():
    db_path = Path("app/file.db")
    if not db_path.exists():
        raise HTTPException(status_code=404, detail="Database file not found")

    return FileResponse(
        path=db_path,
        media_type="application/octet-stream",
        filename="file.db",
    )
