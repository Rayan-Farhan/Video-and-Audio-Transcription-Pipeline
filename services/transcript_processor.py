import re

class TranscriptProcessor:
    def clean_transcript(self, raw):
        text = raw.get('text', '')
        text = re.sub(r"\s+", ' ', text).strip()
        return {'text': text, 'segments': raw.get('segments', [])}

    def chunk_transcript(self, cleaned, source_file: str = "unknown", max_seconds: int = 60):
        segments = cleaned.get('segments', [])
        chunks = []
        current = { 'chunk_id': None, 'text': '', 'timestamp_start': None, 'timestamp_end': None, 'source_file': source_file }
        chunk_idx = 0

        for seg in segments:
            if current['timestamp_start'] is None:
                current['timestamp_start'] = seg['start']
            current['timestamp_end'] = seg['end']
            if current['text']:
                current['text'] += ' '
            current['text'] += seg['text']

            if (current['timestamp_end'] - current['timestamp_start']) >= max_seconds:
                current['chunk_id'] = f"{source_file}_chunk{chunk_idx}"
                current['timestamp_start'] = self._format_seconds(current['timestamp_start'])
                current['timestamp_end'] = self._format_seconds(current['timestamp_end'])
                chunks.append(current.copy())
                chunk_idx += 1
                current = { 'chunk_id': None, 'text': '', 'timestamp_start': None, 'timestamp_end': None, 'source_file': source_file }

        if current['text']:
            current['chunk_id'] = f"{source_file}_chunk{chunk_idx}"
            current['timestamp_start'] = self._format_seconds(current['timestamp_start'])
            current['timestamp_end'] = self._format_seconds(current['timestamp_end'])
            chunks.append(current.copy())

        return chunks

    def _format_seconds(self, seconds: float) -> str:
        seconds = int(round(seconds))
        hrs = seconds // 3600
        mins = (seconds % 3600) // 60
        secs = seconds % 60
        return f"{hrs:02d}:{mins:02d}:{secs:02d}"
