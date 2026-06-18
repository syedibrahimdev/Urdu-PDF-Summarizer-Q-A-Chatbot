import os
import google.genai as genai
from textwrap import wrap
from dotenv import load_dotenv

load_dotenv()

_api_key = os.getenv("GEMINI_API_KEY")
if _api_key:
    genai.configure(api_key=_api_key)

CHUNK_SIZE = 2000


def _get_model():
    """Return configured Gemini model. Raises clear error if API key missing."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "GEMINI_API_KEY not found. Please set it in your .env file or Streamlit secrets."
        )
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.5-flash-lite")


def chunk_text(text: str, size: int = CHUNK_SIZE):
    """Split text into chunks of `size` characters for LLM processing."""
    return wrap(text, size)


def summarize_chunk(chunk: str) -> str:
    """Summarize a single chunk of text in Urdu."""
    try:
        model = _get_model()
        prompt = f"""
براہ کرم اس متن کو اردو میں مختصر اور بامعنی انداز میں خلاصہ کریں۔
اہم نکات کو نمایاں کریں اور اگر ممکن ہو تو thematically group کریں۔

متن:
{chunk}
"""
        response = model.generate_content(prompt)
        return response.text.strip() if response and response.text else ""
    except Exception as e:
        return f"[خلاصہ میں خرابی: {e}]"


def merge_summaries(summaries: list) -> str:
    """Merge multiple chunk summaries into one final structured Urdu summary."""
    try:
        model = _get_model()
        joined = "\n\n".join([s for s in summaries if s])
        if not joined:
            return "کوئی خلاصہ تیار نہیں ہو سکا۔"

        prompt = f"""
یہ مختلف حصوں کے خلاصے ہیں۔ براہ کرم ان سب کو ملا کر ایک مکمل، مربوط اور
سمجھنے میں آسان اردو خلاصہ بنا دیں۔
خلاصہ headings کے ساتھ topic-wise ہونا چاہیے (مثلاً فوائد، نقصانات، تعلیم، صحت وغیرہ)۔

خلاصے:
{joined}
"""
        response = model.generate_content(prompt)
        return response.text.strip() if response and response.text else "خلاصہ دستیاب نہیں۔"
    except Exception as e:
        return f"[خلاصہ ملانے میں خرابی: {e}]"


def summarize_text_urdu(text: str) -> str:
    """Full pipeline: chunk → summarize each → merge into final summary."""
    chunks = chunk_text(text)
    if not chunks:
        return "متن بہت مختصر ہے یا خالی ہے۔"
    summaries = [summarize_chunk(ch) for ch in chunks]
    return merge_summaries(summaries)


def answer_question(text: str, query: str) -> str:
    """Answer a question based strictly on the provided document text."""
    if not query or not query.strip():
        return "براہ کرم ایک سوال درج کریں۔"
    try:
        model = _get_model()
        prompt = f"""
آپ کو ایک دستاویز کا متن اور ایک سوال دیا گیا ہے۔
براہ کرم سوال کا جواب اردو میں دیں اور صرف اسی متن کی بنیاد پر دیں۔
اگر جواب متن میں موجود نہیں تو صاف کہیں کہ "یہ معلومات دستاویز میں موجود نہیں۔"

سوال: {query}

متن:
{text}
"""
        response = model.generate_content(prompt)
        return response.text.strip() if response and response.text else "معذرت، جواب نہیں ملا۔"
    except Exception as e:
        return f"[جواب حاصل کرنے میں خرابی: {e}]"