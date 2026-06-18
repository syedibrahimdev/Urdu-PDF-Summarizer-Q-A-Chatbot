import pdfplumber
import pytesseract
from pdf2image import convert_from_path
from typing import List


def extract_text_from_file(path: str, ocr_threshold_chars: int = 20) -> str:
    """
    Extract text from a single PDF file.

    Strategy:
    1. Try pdfplumber text extraction per page (fast, free, works for real text PDFs).
    2. If a page returns very little text (< ocr_threshold_chars), it's likely a
       scanned/image page — fall back to OCR (Tesseract, Urdu + English) for that page only.

    This keeps things fast for normal PDFs and only pays the OCR cost when needed.
    """
    text = ""
    pages_needing_ocr = []

    try:
        with pdfplumber.open(path) as pdf:
            for i, page in enumerate(pdf.pages):
                page_text = page.extract_text() or ""
                if len(page_text.strip()) < ocr_threshold_chars:
                    pages_needing_ocr.append(i)
                    text += f"\n[[OCR_PLACEHOLDER_{i}]]\n"
                else:
                    text += page_text + "\n"
    except Exception as e:
        raise RuntimeError(f"PDF reading failed: {e}")

    # Run OCR only on pages that need it
    if pages_needing_ocr:
        try:
            ocr_text_map = _ocr_pages(path, pages_needing_ocr)
            for i, ocr_text in ocr_text_map.items():
                text = text.replace(f"[[OCR_PLACEHOLDER_{i}]]", ocr_text)
        except Exception as e:
            # If OCR fails entirely, remove placeholders so they don't pollute output
            for i in pages_needing_ocr:
                text = text.replace(f"[[OCR_PLACEHOLDER_{i}]]", "")
            raise RuntimeError(f"OCR failed: {e}")

    return text.strip()


def _ocr_pages(path: str, page_indices: List[int], dpi: int = 200) -> dict:
    """
    Run Tesseract OCR (Urdu + English) on specific pages of a PDF.
    Returns { page_index: extracted_text }.
    """
    if not page_indices:
        return {}

    results = {}
    # convert_from_path is 1-indexed for first_page/last_page, so we render
    # only the needed pages individually to save memory on large PDFs.
    for idx in page_indices:
        images = convert_from_path(
            path, dpi=dpi, first_page=idx + 1, last_page=idx + 1
        )
        if images:
            ocr_result = pytesseract.image_to_string(images[0], lang="urd+eng")
            results[idx] = ocr_result.strip()
        else:
            results[idx] = ""
    return results


def extract_text_from_multiple(paths: List[str]) -> dict:
    """
    Extract text from multiple PDF files.
    Returns a dict: { filename: extracted_text }
    Skips files that fail and reports them separately.
    """
    results = {}
    errors = {}

    for path in paths:
        filename = path.split("/")[-1]
        try:
            text = extract_text_from_file(path)
            if text:
                results[filename] = text
            else:
                errors[filename] = "No extractable text found, even after OCR"
        except RuntimeError as e:
            errors[filename] = str(e)

    return results, errors


def merge_texts(texts: dict) -> str:
    """
    Merge multiple extracted texts into one combined document.
    Adds a filename header before each document's content.
    """
    merged = ""
    for filename, text in texts.items():
        merged += f"\n\n=== {filename} ===\n\n{text}"
    return merged.strip()