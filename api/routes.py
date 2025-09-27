from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from config import settings
from services.file_handler import save_upload_file
from models.transcription_model import TranscriptionModel
from services.transcript_processor import TranscriptProcessor
from services.storage import Storage
from api.schemas import TranscribeResponse

router = APIRouter()

transcription_model = TranscriptionModel(model_name=settings.MODEL_NAME)
processor = TranscriptProcessor()
storage = Storage(settings=settings)

@router.post('/video/transcribe', response_model=TranscribeResponse)
async def transcribe_endpoint(file: UploadFile = File(...)):
    filename = file.filename
    if not any(filename.lower().endswith('.' + ext) for ext in settings.ALLOWED_EXTENSIONS):
        raise HTTPException(status_code=400, detail="Unsupported file type")

    saved_path, file_id = save_upload_file(file, settings.STORAGE_DIR)

    # *transcribe* returns a dict that includes 'text' and 'segments' and 'latency_seconds'
    raw_result = transcription_model.transcribe(saved_path)

    cleaned = processor.clean_transcript(raw_result)
    chunks = processor.chunk_transcript(cleaned, source_file=filename)

    latency = raw_result.get("latency_seconds", None)

    storage.save_transcript(file_id=file_id, filename=filename, raw=raw_result, cleaned=cleaned, chunks=chunks, latency_seconds=latency)

    return TranscribeResponse(file_id=file_id, message="Transcription completed", latency_seconds=latency)

@router.get('/video/{file_id}/transcript')
async def get_transcript(file_id: str):
    transcript = storage.get_transcript(file_id)
    if transcript is None:
        raise HTTPException(status_code=404, detail="Transcript not found")
    return JSONResponse(content=transcript)

@router.get('/video/{file_id}/chunks')
async def get_chunks(file_id: str):
    chunks = storage.get_chunks(file_id)
    if chunks is None:
        raise HTTPException(status_code=404, detail="Chunks not found")
    return JSONResponse(content={"chunks": chunks})