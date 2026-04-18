"""
PDF Processor — extracts and cleans text from uploaded ESG PDF reports.
Uses PyMuPDF (fitz) for reliable text extraction.
"""
import re
import io


def extract_text_from_pdf(uploaded_file) -> str:
    """Extract text from a Streamlit UploadedFile or file path."""
    try:
        import fitz  # PyMuPDF
    except ImportError:
        return _fallback_extraction(uploaded_file)

    try:
        if hasattr(uploaded_file, "read"):
            data = uploaded_file.read()
            doc = fitz.open(stream=data, filetype="pdf")
        else:
            doc = fitz.open(uploaded_file)

        pages = []
        for page in doc:
            text = page.get_text("text")
            pages.append(text)

        raw = "\n\n".join(pages)
        return clean_text(raw)

    except Exception as e:
        return f"[Error extracting PDF: {e}]"


def _fallback_extraction(uploaded_file) -> str:
    """Fallback using pdfplumber if PyMuPDF not available."""
    try:
        import pdfplumber
        data = uploaded_file.read() if hasattr(uploaded_file, "read") else open(uploaded_file,"rb").read()
        with pdfplumber.open(io.BytesIO(data)) as pdf:
            return clean_text("\n\n".join(p.extract_text() or "" for p in pdf.pages))
    except Exception as e:
        return f"[PDF extraction failed: {e}. Install pymupdf: pip install pymupdf]"


def clean_text(text: str) -> str:
    """Remove noise: multiple spaces, page numbers, headers/footers."""
    text = re.sub(r'\n{3,}', '\n\n', text)          # collapse blank lines
    text = re.sub(r'[ \t]{2,}', ' ', text)           # collapse spaces
    text = re.sub(r'Page \d+ of \d+', '', text)      # remove page numbers
    text = re.sub(r'^\s*\d+\s*$', '', text, flags=re.MULTILINE)  # lone numbers
    return text.strip()


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """Split text into overlapping chunks for embedding."""
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)
    return chunks
