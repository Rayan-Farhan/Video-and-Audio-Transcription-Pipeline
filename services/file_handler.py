import os, uuid
from fastapi import UploadFile
from pathlib import Path

def ensure_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)

def save_upload_file(upload_file: UploadFile, storage_dir: str):
    ensure_dir(storage_dir)
    file_id = str(uuid.uuid4())
    _, ext = os.path.splitext(upload_file.filename)
    saved_name = f"{file_id}{ext}"
    saved_path = os.path.join(storage_dir, saved_name)
    with open(saved_path, 'wb') as out_file:
        content = upload_file.file.read()
        out_file.write(content)
    return saved_path, file_id
