import uuid
from fastapi import APIRouter, Request, UploadFile, File, Form
from src.models.schemas import JDUploadResponse
from src.services.parser import parse_file, parse_text
from src.services.chunker import chunk_jd
from src.services.vectordb import VectorStore

router = APIRouter(prefix="/api/jd", tags=["jd"])

_jds: dict = {}


@router.post("/upload", response_model=JDUploadResponse)
async def upload_jd(
    request: Request,
    file: UploadFile | None = File(None),
    text: str | None = Form(None),
):
    jd_id = str(uuid.uuid4())[:8]
    title = "text_input"

    if file and file.filename:
        file_bytes = await file.read()
        title = file.filename
        parsed = parse_file(file_bytes, title)
    else:
        body_text = text
        if body_text is None and request.headers.get("content-type", "").startswith("application/json"):
            payload = await request.json()
            body_text = payload.get("text") if isinstance(payload, dict) else None
        parsed = parse_text(body_text) if body_text else ""
        if body_text:
            lines = parsed.split("\n")
            title = lines[0][:50] if lines else "text_input"
    _jds[jd_id] = {"title": title, "parsed_text": parsed}

    chunks = chunk_jd(parsed)
    if chunks:
        vs = VectorStore()
        vs.add_chunks("jd_chunks", chunks, f"jd_{jd_id}")

    return JDUploadResponse(jd_id=jd_id, title=title, parsed_text=parsed)
