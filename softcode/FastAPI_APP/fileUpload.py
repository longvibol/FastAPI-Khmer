from fastapi import FastAPI, UploadFile, File

app = FastAPI()

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    # Read file content to calculate size
    contents = await file.read()

    # Size in bytes
    file_size_bytes = len(contents)

    # Convert bytes to GB
    file_size_gb = file_size_bytes / (1024 ** 3)

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "file_size_bytes": file_size_bytes,
        "file_size_gb": round(file_size_gb, 6)
    }