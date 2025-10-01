# Video & Audio Transcription Pipeline

A high-performance FastAPI-based transcription service that converts video and audio files into accurate text transcripts using OpenAI's Whisper model. The system provides both raw transcripts and intelligently chunked segments for easy processing and analysis.

## Features

- **Fast Transcription**: Powered by OpenAI Whisper with optimized performance
- **Multiple Format Support**: Handles MP4, MKV, AVI, MP3, and WAV files
- **Intelligent Chunking**: Automatically segments transcripts into manageable chunks
- **RESTful API**: Clean, well-documented API endpoints
- **Real-time Processing**: Fast processing with latency tracking
- **Persistent Storage**: Saves transcripts and metadata for later retrieval

## Performance Metrics

Based on evaluation results:
- **Accuracy**: ]12.3% Word Error Rate for noisy background videos
- **Model**: Whisper "tiny" (configurable to other sizes)
- **Supported Languages**: Auto-detection with high accuracy

## Quick Start

### Prerequisites

- Python 3.8 or higher
- FFmpeg installed and added to system PATH
- 4GB+ RAM recommended

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd transcription_pipeline
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install FFmpeg:
   - **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH
   - **macOS**: `brew install ffmpeg`
   - **Linux**: `sudo apt install ffmpeg`

### Running the Application

Start the development server:
```bash
uvicorn app:app --reload
```

The API will be available at:
- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Base URL**: http://localhost:8000/api

## API Usage

### Upload and Transcribe

```bash
curl -X POST "http://localhost:8000/api/video/transcribe" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@your_video.mp4"
```

Response:
```json
{
  "file_id": "unique-file-id",
  "message": "Transcription completed",
  "latency_seconds": 38.89
}
```

### Get Full Transcript

```bash
curl -X GET "http://localhost:8000/api/video/{file_id}/transcript"
```

### Get Chunked Transcript

```bash
curl -X GET "http://localhost:8000/api/video/{file_id}/chunks"
```

## Configuration

The application can be configured through environment variables or by modifying `config.py`:

```python
APP_HOST = "0.0.0.0"           # Server host
APP_PORT = 8000                # Server port
STORAGE_DIR = "./storage"      # File storage directory
MODEL_NAME = "tiny"            # Whisper model size
MAX_FILE_SIZE_BYTES = 200MB    # Maximum file size
ALLOWED_EXTENSIONS = ["mp4", "mkv", "avi", "mp3", "wav"]
```

## File Structure

```
transcription_pipeline/
├── app.py                 # FastAPI application
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── api/
│   ├── routes.py         # API endpoints
│   └── schemas.py        # Pydantic models
├── models/
│   └── transcription_model.py  # Whisper integration
├── services/
│   ├── file_handler.py   # File upload handling
│   ├── transcript_processor.py  # Text processing
│   └── storage.py        # Data persistence
├── evaluation/
│   ├── evaluate.py       # Accuracy evaluation
│   └── report.json       # Performance metrics
└── storage/              # Uploaded files and transcripts
```

## Evaluation

Run the built-in evaluation script to test accuracy:

```bash
python evaluation/evaluate.py
```

This will:
- Load all transcripts from storage
- Compare against reference text
- Calculate Word Error Rate (WER)
- Generate performance report