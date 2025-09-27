from fastapi import FastAPI
from api.routes import router
from config import settings

app = FastAPI(title="Transcription Pipeline", version="0.1.0")
app.include_router(router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Transcription Pipeline. Visit /docs to get started."}