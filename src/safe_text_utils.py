import re
from typing import List

def is_empty_text(text: str) -> bool:
    if not text or len(text.strip()) == 0:
        return True
    cleaned = re.sub(r"[^ء-یa-zA-Z0-9]", "", text)
    return len(cleaned.strip()) == 0

def split_text_into_chunks(text: str, max_words: int = 1500) -> List[str]:
    words = text.split()
    chunks = []
    for i in range(0, len(words), max_words):
        chunk = " ".join(words[i:i+max_words])
        chunks.append(chunk)
    return chunks
