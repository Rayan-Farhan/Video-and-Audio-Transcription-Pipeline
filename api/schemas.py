from pydantic import BaseModel
from typing import Optional

class TranscribeResponse(BaseModel):
    file_id: str
    message: str
    latency_seconds: Optional[float] = None

class Chunk(BaseModel):
    chunk_id: str
    text: str
    timestamp_start: str
    timestamp_end: str
    source_file: str