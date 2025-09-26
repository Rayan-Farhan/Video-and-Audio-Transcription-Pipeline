import os, json
from pathlib import Path

class Storage:
    def __init__(self, settings):
        self.settings = settings
        Path(self.settings.STORAGE_DIR).mkdir(parents=True, exist_ok=True)
        self.json_dir = os.path.join(self.settings.STORAGE_DIR, 'json')
        Path(self.json_dir).mkdir(parents=True, exist_ok=True)

    def _json_path(self, file_id: str):
        return os.path.join(self.json_dir, f"{file_id}.json")

    def save_transcript(self, file_id: str, filename: str, raw, cleaned, chunks):
        data = {
            'file_id': file_id,
            'filename': filename,
            'raw': raw,
            'cleaned': cleaned,
            'chunks': chunks
        }
        with open(self._json_path(file_id), 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def get_transcript(self, file_id: str):
        p = self._json_path(file_id)
        if not os.path.exists(p):
            return None
        with open(p, 'r', encoding='utf-8') as f:
            return json.load(f)

    def get_chunks(self, file_id: str):
        data = self.get_transcript(file_id)
        if data is None:
            return None
        return data.get('chunks', [])
