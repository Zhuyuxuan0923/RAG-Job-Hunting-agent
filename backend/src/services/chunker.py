import re
from typing import List, Dict, Any


def chunk_resume(text: str, max_tokens: int = 500) -> List[Dict[str, Any]]:
    sections = re.split(r"\n(?=#{1,3}\s)", text)
    chunks = []
    idx = 0
    for section in sections:
        section = section.strip()
        if not section:
            continue
        header_match = re.match(r"^#{1,3}\s+(.+)", section)
        section_name = header_match.group(1) if header_match else "其他"
        content = section
        if len(content) > max_tokens * 4:
            paragraphs = content.split("\n\n")
            for para in paragraphs:
                para = para.strip()
                if para:
                    chunks.append({
                        "text": para,
                        "section": section_name,
                        "chunk_index": idx,
                    })
                    idx += 1
        else:
            chunks.append({
                "text": content,
                "section": section_name,
                "chunk_index": idx,
            })
            idx += 1
    return chunks


def chunk_jd(text: str, chunk_size: int = 800, overlap: int = 100) -> List[Dict[str, Any]]:
    paragraphs = text.split("\n\n")
    chunks = []
    idx = 0
    current_chunk = ""
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        if len(current_chunk) + len(para) > chunk_size * 4 and current_chunk:
            chunks.append({"text": current_chunk.strip(), "chunk_index": idx})
            idx += 1
            overlap_text = current_chunk[-overlap * 4:] if len(current_chunk) > overlap * 4 else current_chunk
            current_chunk = overlap_text + "\n" + para
        else:
            current_chunk += "\n" + para if current_chunk else para
    if current_chunk.strip():
        chunks.append({"text": current_chunk.strip(), "chunk_index": idx})
    return chunks
