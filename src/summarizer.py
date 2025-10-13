import os
import google.generativeai as genai
from textwrap import wrap
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

CHUNK_SIZE = 2000

def chunk_text(text: str, size: int = CHUNK_SIZE):
    return wrap(text, size)

def summarize_chunk(chunk: str) -> str:
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""
    براہ کرم اس متن کو اردو میں مختصر اور بامعنی انداز میں خلاصہ کریں۔
    اہم نکات کو نمایاں کریں اور اگر ممکن ہو تو thematically group کریں۔
    
    متن:
    {chunk}
    """
    response = model.generate_content(prompt)
    return response.text.strip() if response and response.text else ""

def merge_summaries(summaries: list) -> str:
    model = genai.GenerativeModel("gemini-1.5-flash")
    joined = "\n\n".join(summaries)
    prompt = f"""
    یہ مختلف حصوں کے خلاصے ہیں۔ براہ کرم ان سب کو ملا کر ایک مکمل، مربوط اور
    سمجھنے میں آسان اردو خلاصہ بنا دیں۔ 
    خلاصہ headings کے ساتھ topic-wise ہونا چاہیے (مثلاً فوائد، نقصانات، تعلیم، صحت وغیرہ)۔
    
    خلاصے:
    {joined}
    """
    response = model.generate_content(prompt)
    return response.text.strip() if response and response.text else ""

def summarize_text_urdu(text: str) -> str:
    chunks = chunk_text(text)
    summaries = [summarize_chunk(ch) for ch in chunks]
    final_summary = merge_summaries(summaries)
    return final_summary

def answer_question(text: str, query: str) -> str:
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""
    آپ کو ایک دستاویز کا متن اور ایک سوال دیا گیا ہے۔
    براہ کرم سوال کا جواب اردو میں دیں اور صرف اسی متن کی بنیاد پر دیں۔
    
    سوال: {query}
    متن:
    {text}
    """
    response = model.generate_content(prompt)
    return response.text.strip() if response and response.text else "معذرت، جواب نہیں ملا۔"
