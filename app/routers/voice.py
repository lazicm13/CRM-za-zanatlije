import os
import tempfile
from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel

from app.services.transcription import transcribe_audio_file
from app.services.job_parser import parse_job_from_text


router = APIRouter(prefix="/api/voice", tags=["voice"])


class ParseTextRequest(BaseModel):
    text: str


@router.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    suffix = os.path.splitext(file.filename or "audio.webm")[1] or ".webm"

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        text = transcribe_audio_file(tmp_path)
        return {"text": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {e}")
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


@router.post("/parse-job")
async def parse_job(payload: ParseTextRequest):
    try:
        parsed = parse_job_from_text(payload.text)
        return parsed
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Parsing failed: {e}")