import pdfplumber

def extract_text_pdf(path, ocr_threshold_chars=100):
    """
    Extract text from PDF using pdfplumber only (no OCR).
    """
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            text += page_text + "\n"
    return text.strip()
