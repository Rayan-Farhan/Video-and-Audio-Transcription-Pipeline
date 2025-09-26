import uvicorn
from fastapi import FastAPI
from api.routes import router
from config import settings

app = FastAPI(title="Transcription Pipeline")
app.include_router(router, prefix="/api")

if __name__ == '__main__':
    uvicorn.run('app:app', host=settings.APP_HOST, port=settings.APP_PORT, reload=True)