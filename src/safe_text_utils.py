import re
from typing import List


def is_empty_text(text: str) -> bool:
    """
    Returns True if text has no meaningful Urdu or Latin characters.
    Strips all punctuation/symbols before checking.
    """
    if not text or len(text.strip()) == 0:
        return True
    cleaned = re.sub(r"[^ء-یa-zA-Z0-9]", "", text)
    return len(cleaned.strip()) == 0


def get_word_count(text: str) -> int:
    """Return approximate word count of the text."""
    return len(text.split())


def split_text_into_chunks(text: str, max_words: int = 1500) -> List[str]:
    """
    Split text into chunks of max_words words each.
    Used to stay within LLM context limits.
    """
    words = text.split()
    chunks = []
    for i in range(0, len(words), max_words):
        chunk = " ".join(words[i : i + max_words])
        chunks.append(chunk)
    return chunks


def truncate_for_qa(text: str, max_words: int = 3000) -> str:
    """
    Truncate text to max_words for Q&A context.
    Gemini handles large contexts but we keep it focused.
    """
    words = text.split()
    if len(words) <= max_words:
        return text
    return " ".join(words[:max_words])