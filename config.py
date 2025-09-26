from pydantic import BaseSettings
from typing import List

class Settings(BaseSettings):
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    STORAGE_DIR: str = "./storage"
    MODEL_NAME: str = "small"  # tiny, base, small, medium, large
    MAX_FILE_SIZE_BYTES: int = 200 * 1024 * 1024  # 200 MB
    ALLOWED_EXTENSIONS: List[str] = ["mp4","mkv","avi","mp3","wav"]
    DATABASE_URL: str = "sqlite:///./storage/transcripts.db"
    USE_POSTGRES: bool = False

settings = Settings()
