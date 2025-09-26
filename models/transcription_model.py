import os
import whisper

# Make sure ffmpeg is visible to Python
os.environ["PATH"] += os.pathsep + r"C:\Users\abdul\Downloads\ffmpeg-2025-09-25-git-9970dc32bf-full_build\ffmpeg-2025-09-25-git-9970dc32bf-full_build\bin"

class TranscriptionModel:
    def __init__(self, model_name="tiny", device="cpu"):
        self.model = whisper.load_model(model_name, device=device)

    def transcribe(self, file_path: str):
        result = self.model.transcribe(file_path)
        return result
