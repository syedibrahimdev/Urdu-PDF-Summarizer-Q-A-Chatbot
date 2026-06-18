import re
from cleantext import clean


def clean_text(text: str) -> str:
    """
    Fix common PDF extraction artifacts:
    - Remove hyphenated line breaks (e.g. "some- \nthing")
    - Collapse multiple blank lines into one
    - Remove extra spaces
    """
    text = re.sub(r"-\n", "", text)
    text = re.sub(r"\n{2,}", "\n\n", text)
    text = re.sub(r"[ ]{2,}", " ", text)
    return text.strip()


def normalize_urdu(text: str) -> str:
    """
    Normalize Urdu/bilingual text using clean-text:
    - Fix unicode (ligatures, zero-width chars, etc.)
    - Preserve RTL characters (to_ascii=False)
    - Remove URLs and emails
    - Collapse repeated whitespace
    """
    text = clean(
        text,
        fix_unicode=True,
        to_ascii=False,
        lower=False,
        no_line_breaks=False,
        keep_two_line_breaks=True,
        no_urls=True,
        no_emails=True,
    )
    text = re.sub(r"\s{2,}", " ", text)
    return text.strip()