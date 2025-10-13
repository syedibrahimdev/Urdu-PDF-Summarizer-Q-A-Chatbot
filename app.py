import streamlit as st
from src.ingestion import extract_text_pdf
from src.preprocessing import clean_text, normalize_urdu
from src.safe_text_utils import is_empty_text, split_text_into_chunks
from src.summarizer import summarize_text_urdu
import os

st.set_page_config(page_title="📚 Urdu PDF Chatbot", layout="wide")

st.title("📚 Urdu PDF Summarizer & Q&A Chatbot")

# File uploader
uploaded_file = st.file_uploader("📂 ایک PDF اپ لوڈ کریں", type=["pdf"])

if uploaded_file:
    # Save temp file
    temp_path = os.path.join("temp_uploaded.pdf")
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    text = extract_text_pdf(temp_path)
    text = clean_text(text)
    text = normalize_urdu(text)

    if is_empty_text(text):
        st.error("❌ اس PDF سے متن نہیں نکالا جا سکا۔ براہ کرم دوسرا فائل اپ لوڈ کریں۔")
    else:
        st.success("✅ متن کامیابی سے نکالا گیا!")
        tab1, tab2 = st.tabs(["📝 خلاصہ", "❓ سوال جواب"])

        with tab1:
            if st.button("خلاصہ بنائیں"):
                summary = summarize_text_urdu(text)
                st.subheader("خلاصہ")
                st.write(summary)

        with tab2:
            query = st.text_input("اپنا سوال درج کریں")
            if st.button("جواب حاصل کریں"):
                from src.summarizer import answer_question
                answer = answer_question(text, query)
                st.subheader("جواب")
                st.write(answer)
