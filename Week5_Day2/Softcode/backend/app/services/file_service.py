from pathlib import Path
from uuid import uuid4
from fastapi import UploadFile
import shutil

UPLOAD_ROOT = Path(__file__).resolve().parent.parent / "uploads" / "products"
MAIN_DIR = UPLOAD_ROOT / "main"
SUB_DIR = UPLOAD_ROOT / "sub"

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def save_upload_file(file: UploadFile, sub_folder: str = "main") -> str:
    ext = Path(file.filename or "").suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError("Only jpg, jpeg, png and webp images are allowed")

    folder = MAIN_DIR if sub_folder == "main" else SUB_DIR
    folder.mkdir(parents=True, exist_ok=True)

    new_name = f"{uuid4().hex}{ext}"
    file_path = folder / new_name

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return f"/uploads/products/{sub_folder}/{new_name}"
