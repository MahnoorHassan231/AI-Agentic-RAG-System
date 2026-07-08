"""
document_loader.py
-------------------
Responsible for:
1. Opening a PDF
2. Extracting its text
3. Splitting that text into chunks

This is not AI — just a reader/splitter.
"""

from pypdf import PdfReader
import config


def load_pdf_text(pdf_path: str) -> str:
    """Extracts all text from a PDF file and returns it as a single string."""
    reader = PdfReader(pdf_path)
    full_text = ""
    for page in reader.pages:
        page_text = page.extract_text() or ""
        full_text += page_text + "\n"
    return full_text


def chunk_text(text: str, chunk_size: int = None, overlap: int = None) -> list[str]:
    """
    Splits long text into smaller overlapping chunks.
    Overlap prevents context from being lost between adjacent chunks.
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
    """Extracts text from a PDF and returns it as chunks. Main entry point."""
    text = load_pdf_text(pdf_path)
    return chunk_text(text)