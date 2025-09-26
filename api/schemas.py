from pydantic import BaseModel

class TranscribeResponse(BaseModel):
    file_id: str
    message: str

class Chunk(BaseModel):
    chunk_id: str
    text: str
    timestamp_start: str
    timestamp_end: str
    source_file: str