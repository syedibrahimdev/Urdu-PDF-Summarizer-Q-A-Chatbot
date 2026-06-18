import os
import tempfile
import streamlit as st

from src.ingestion import extract_text_from_multiple, merge_texts
from src.preprocessing import clean_text, normalize_urdu
from src.safe_text_utils import is_empty_text, get_word_count, truncate_for_qa
from src.summarizer import summarize_text_urdu, answer_question

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="📚 Urdu PDF Chatbot",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Session state init ────────────────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []      # list of {"role": "user"/"assistant", "content": str}
if "document_text" not in st.session_state:
    st.session_state.document_text = ""
if "summary" not in st.session_state:
    st.session_state.summary = ""
if "processed_files" not in st.session_state:
    st.session_state.processed_files = []

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("📚 Urdu PDF Assistant")
    st.markdown("---")

    st.subheader("📂 PDFs اپ لوڈ کریں")
    uploaded_files = st.file_uploader(
        "ایک یا زیادہ PDF فائلیں منتخب کریں",
        type=["pdf"],
        accept_multiple_files=True,
        help="آپ ایک ساتھ کئی PDFs اپ لوڈ کر سکتے ہیں",
    )

    if uploaded_files:
        if st.button("📥 فائلیں پروسیس کریں", use_container_width=True):
            # Save temp files
            temp_paths = []
            for uf in uploaded_files:
                suffix = ".pdf"
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                    tmp.write(uf.getbuffer())
                    temp_paths.append((uf.name, tmp.name))

            with st.spinner("متن نکالا جا رہا ہے... (تصویری صفحات کے لیے OCR استعمال ہو سکتا ہے)"):
                path_map = {name: path for name, path in temp_paths}
                extracted, errors = extract_text_from_multiple(list(path_map.values()))

                # Rename keys back to original filenames
                renamed = {}
                for orig_name, tmp_path in temp_paths:
                    tmp_filename = tmp_path.split("/")[-1]
                    for key in extracted:
                        if tmp_path.endswith(key) or key in tmp_path:
                            renamed[orig_name] = extracted[key]
                            break
                # Fallback: use extracted as-is if rename didn't work
                if not renamed:
                    renamed = extracted

            if errors:
                for fname, err in errors.items():
                    st.error(f"❌ {fname}: {err}")

            if renamed:
                with st.spinner("متن صاف کیا جا رہا ہے..."):
                    cleaned = {}
                    for fname, text in renamed.items():
                        t = clean_text(text)
                        t = normalize_urdu(t)
                        if not is_empty_text(t):
                            cleaned[fname] = t

                if cleaned:
                    merged = merge_texts(cleaned)
                    st.session_state.document_text = merged
                    st.session_state.processed_files = list(cleaned.keys())
                    st.session_state.chat_history = []  # reset chat on new upload
                    st.session_state.summary = ""
                    st.success(f"✅ {len(cleaned)} فائل(یں) تیار ہیں!")
                else:
                    st.error("❌ کسی بھی فائل سے متن نہیں نکالا جا سکا۔")

            # Cleanup temp files
            for _, tmp_path in temp_paths:
                try:
                    os.unlink(tmp_path)
                except Exception:
                    pass

    st.markdown("---")

    if st.session_state.processed_files:
        st.subheader("✅ پروسیس شدہ فائلیں")
        for f in st.session_state.processed_files:
            st.markdown(f"• {f}")

        word_count = get_word_count(st.session_state.document_text)
        st.caption(f"کل الفاظ: {word_count:,}")

        if st.button("🗑️ سب صاف کریں", use_container_width=True):
            st.session_state.document_text = ""
            st.session_state.chat_history = []
            st.session_state.summary = ""
            st.session_state.processed_files = []
            st.rerun()

    st.markdown("---")
    st.caption("Built by [syedibrahimdev](https://github.com/syedibrahimdev)")

# ── Main area ─────────────────────────────────────────────────────────────────
st.title("📚 Urdu PDF Summarizer & Q&A")

if not st.session_state.document_text:
    st.info("👈 بائیں طرف PDF فائلیں اپ لوڈ کریں اور 'فائلیں پروسیس کریں' بٹن دبائیں۔")

    st.markdown("### یہ ایپ کیا کرتی ہے؟")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("#### 📄 PDF اپ لوڈ")
        st.markdown("ایک یا زیادہ اردو/دوزبانی PDF فائلیں اپ لوڈ کریں")
    with col2:
        st.markdown("#### 📝 خودکار خلاصہ")
        st.markdown("Google Gemini سے مکمل topic-wise اردو خلاصہ حاصل کریں")
    with col3:
        st.markdown("#### ❓ سوال جواب")
        st.markdown("دستاویز سے متعلق کوئی بھی سوال اردو میں پوچھیں")
    st.stop()

# Tabs
tab1, tab2 = st.tabs(["📝 خلاصہ", "💬 سوال جواب (Chat)"])

# ── Tab 1: Summary ────────────────────────────────────────────────────────────
with tab1:
    st.subheader("📝 دستاویز کا خلاصہ")

    if st.session_state.summary:
        st.markdown(st.session_state.summary)
        if st.button("🔄 دوبارہ بنائیں"):
            st.session_state.summary = ""
            st.rerun()
    else:
        if st.button("✨ خلاصہ بنائیں", use_container_width=True):
            with st.spinner("خلاصہ تیار ہو رہا ہے... (یہ 30-60 سیکنڈ لے سکتا ہے)"):
                try:
                    summary = summarize_text_urdu(st.session_state.document_text)
                    st.session_state.summary = summary
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ خلاصہ بنانے میں خرابی: {e}")

# ── Tab 2: Chat Q&A ───────────────────────────────────────────────────────────
with tab2:
    st.subheader("💬 دستاویز سے سوال پوچھیں")

    # Render chat history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    query = st.chat_input("اپنا سوال یہاں لکھیں...")

    if query:
        # Show user message
        st.session_state.chat_history.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)

        # Get answer
        with st.chat_message("assistant"):
            with st.spinner("جواب تلاش کیا جا رہا ہے..."):
                try:
                    context = truncate_for_qa(st.session_state.document_text, max_words=3000)
                    answer = answer_question(context, query)
                except Exception as e:
                    answer = f"❌ جواب حاصل کرنے میں خرابی: {e}"
                st.markdown(answer)

        st.session_state.chat_history.append({"role": "assistant", "content": answer})

    # Clear chat button
    if st.session_state.chat_history:
        if st.button("🗑️ گفتگو صاف کریں"):
            st.session_state.chat_history = []
            st.rerun()