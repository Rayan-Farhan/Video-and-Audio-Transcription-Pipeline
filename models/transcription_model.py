import os
import time
import whisper
import torch
from typing import Dict, Any

os.environ["PATH"] += os.pathsep + r"C:\Users\abdul\Downloads\ffmpeg-2025-09-25-git-9970dc32bf-full_build\ffmpeg-2025-09-25-git-9970dc32bf-full_build\bin"

class TranscriptionModel:
    def __init__(self, model_name: str = "tiny", device: str = None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model_name = model_name
        self.model = None
        self._load_model()

    def _load_model(self):
        if self.model is None:
            self.model = whisper.load_model(self.model_name, device=self.device)

    def transcribe(self, file_path: str) -> Dict[str, Any]:
        self._load_model()
        t0 = time.time()
        result = self.model.transcribe(file_path)
        t1 = time.time()
        latency = t1 - t0

        structured = {
            "text": result.get("text", "").strip(),
            "segments": [],
            "language": result.get("language", None),
            "latency_seconds": latency
        }

        for seg in result.get("segments", []):
            structured["segments"].append({
                "id": seg.get("id"),
                "start": float(seg.get("start", 0.0)),
                "end": float(seg.get("end", 0.0)),
                "text": seg.get("text", "").strip()
            })
        return structured