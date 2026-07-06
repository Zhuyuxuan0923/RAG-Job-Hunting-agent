import io


def parse_pdf(file_bytes: bytes, filename: str) -> str:
    import fitz
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text_parts = []
    for page in doc:
        text_parts.append(page.get_text())
    doc.close()
    return "\n".join(text_parts).strip()


def parse_docx(file_bytes: bytes, filename: str) -> str:
    from docx import Document
    doc = Document(io.BytesIO(file_bytes))
    text_parts = []
    for para in doc.paragraphs:
        if para.text.strip():
            text_parts.append(para.text)
    return "\n".join(text_parts).strip()


def parse_text(text: str) -> str:
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    return "\n".join(lines)


def parse_file(file_bytes: bytes, filename: str) -> str:
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext == "pdf":
        return parse_pdf(file_bytes, filename)
    elif ext in ("docx", "doc"):
        return parse_docx(file_bytes, filename)
    else:
        raise ValueError(f"Unsupported file type: .{ext}")
