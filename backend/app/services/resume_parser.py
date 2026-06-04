
from pathlib import Path
from pypdf import PdfReader


def extract_text_from_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    text_parts = []

    for page in reader.pages:
        page_text = page.extract_text() or ""
        text_parts.append(page_text)

    return "\n".join(text_parts).strip()


def extract_text_from_txt(file_path: str) -> str:
    path = Path(file_path)
    return path.read_text(encoding="utf-8", errors="ignore").strip()


def extract_resume_text(file_path: str, filename: str) -> str:
    lower_name = filename.lower()

    if lower_name.endswith(".pdf"):
        return extract_text_from_pdf(file_path)

    if lower_name.endswith(".txt"):
        return extract_text_from_txt(file_path)

    raise ValueError("Unsupported file type. Please upload a PDF or TXT file.")