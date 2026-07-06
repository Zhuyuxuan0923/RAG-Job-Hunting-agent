import uuid
from fastapi import APIRouter, UploadFile, File, Form
from src.models.schemas import ResumeUploadResponse
from src.services.parser import parse_file, parse_text
from src.services.chunker import chunk_resume
from src.services.vectordb import VectorStore

router = APIRouter(prefix="/api/resume", tags=["resume"])

_resumes: dict = {}


@router.post("/upload", response_model=ResumeUploadResponse)
async def upload_resume(
    file: UploadFile | None = File(None),
    text: str | None = Form(None),
):
    resume_id = str(uuid.uuid4())[:8]
    filename = "text_input"

    if file and file.filename:
        file_bytes = await file.read()
        filename = file.filename
        parsed = parse_file(file_bytes, filename)
    elif text:
        parsed = parse_text(text)
    else:
        parsed = ""

    _resumes[resume_id] = {"filename": filename, "parsed_text": parsed}

    chunks = chunk_resume(parsed)
    if chunks:
        vs = VectorStore()
        vs.add_chunks("resume_chunks", chunks, f"resume_{resume_id}")

    return ResumeUploadResponse(resume_id=resume_id, filename=filename, parsed_text=parsed)
