"""
document_loader.py
-------------------
Iska kaam sirf itna hai:
1. PDF kholna
2. Text nikalna
3. Text ko chunks mein todna

Ye AI nahi hai. Sirf "reader" hai.
"""

from pypdf import PdfReader
import config


def load_pdf_text(pdf_path: str) -> str:
    """PDF file se poora text nikal kar ek string mein return karta hai."""
    reader = PdfReader(pdf_path)
    full_text = ""
    for page in reader.pages:
        page_text = page.extract_text() or ""
        full_text += page_text + "\n"
    return full_text


def chunk_text(text: str, chunk_size: int = None, overlap: int = None) -> list[str]:
    """
    Bade text ko chhote chunks mein todta hai.
    Overlap isliye rakhte hain taake do chunks ke beech context na toote.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += chunk_size - overlap

    return chunks


def load_and_chunk_pdf(pdf_path: str) -> list[str]:
    """PDF se text nikal kar seedha chunks return kar deta hai. Sabse zyada use hone wala function."""
    text = load_pdf_text(pdf_path)
    return chunk_text(text)
