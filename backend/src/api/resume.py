import uuid
from fastapi import APIRouter, Request, UploadFile, File, Form
from src.models.schemas import ResumeUploadResponse
from src.services.parser import parse_file, parse_text
from src.services.chunker import chunk_resume
from src.services.vectordb import VectorStore

router = APIRouter(prefix="/api/resume", tags=["resume"])

_resumes: dict = {}


@router.post("/upload", response_model=ResumeUploadResponse)
async def upload_resume(
    request: Request,
    file: UploadFile | None = File(None),
    text: str | None = Form(None),
):
    resume_id = str(uuid.uuid4())[:8]
    filename = "text_input"

    if file and file.filename:
        file_bytes = await file.read()
        filename = file.filename
        parsed = parse_file(file_bytes, filename)
    else:
        body_text = text
        if body_text is None and request.headers.get("content-type", "").startswith("application/json"):
            payload = await request.json()
            body_text = payload.get("text") if isinstance(payload, dict) else None
        parsed = parse_text(body_text) if body_text else ""

    _resumes[resume_id] = {"filename": filename, "parsed_text": parsed}

    chunks = chunk_resume(parsed)
    if chunks:
        vs = VectorStore()
        vs.add_chunks("resume_chunks", chunks, f"resume_{resume_id}")

    return ResumeUploadResponse(resume_id=resume_id, filename=filename, parsed_text=parsed)
