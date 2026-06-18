<div align="center">

# 📚 Urdu PDF Summarizer & Q&A Chatbot

**AI-powered Urdu document assistant — upload any PDF, get a structured Urdu summary or ask questions in Urdu.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Gemini](https://img.shields.io/badge/Google%20Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

[🚀 Live Demo](https://syedibrahimdev-urdu-pdf-summarizer.streamlit.app) · [📂 Source Code](https://github.com/syedibrahimdev/Urdu-PDF-Summarizer-Q-A-Chatbot) · [🐛 Report Bug](https://github.com/syedibrahimdev/Urdu-PDF-Summarizer-Q-A-Chatbot/issues)

</div>

---

## 🧐 What Is This?

Most AI tools fail at Urdu — they either transliterate badly or ignore the language entirely.

**Urdu PDF Summarizer** fixes that. Upload any Urdu or bilingual PDF and the app will:
- Extract and clean the Urdu text properly (preserving RTL characters)
- Automatically run **OCR on scanned/image-based pages** using Tesseract (Urdu + English)
- Generate a **structured, topic-wise Urdu summary** using Google Gemini
- Let you **ask questions in Urdu** and get answers grounded in the document

Built for students, researchers, and professionals who work with Urdu content.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📄 PDF Text Extraction | Extracts Urdu/bilingual text using `pdfplumber` |
| 🔍 Smart OCR Fallback | Automatically detects image-based pages and runs Tesseract OCR (urd+eng) |
| 🧹 Urdu Text Normalization | Cleans unicode artifacts, extra spaces, broken line breaks |
| 📝 Structured Summarization | Chunk-based summarization merged into topic-wise headings |
| ❓ Document Q&A (Chat) | Chat-style Q&A with history — answers grounded in the uploaded PDF only |
| 📂 Multi-PDF Support | Upload multiple PDFs at once — merged and processed together |
| ↔️ RTL Text Rendering | Proper right-to-left display for Urdu text in UI |
| ⚡ Streamlit UI | Simple, tabbed interface — no technical knowledge needed |

---

## 🏗️ Architecture
📂 Upload PDF(s)

│

▼

┌─────────────────┐

│   ingestion.py  │  ← pdfplumber extracts text page by page

│                 │     if page text < 20 chars → Tesseract OCR fallback (urd+eng)

└────────┬────────┘

│

▼

┌──────────────────────┐

│   preprocessing.py   │  ← Cleans hyphenation, extra whitespace

│   safe_text_utils.py │  ← Validates text, splits into chunks

└────────┬─────────────┘

│

▼

┌─────────────────┐

│  summarizer.py  │  ← Gemini 2.5 Flash Lite

│                 │     • summarize_chunk()  — per-chunk Urdu summary

│                 │     • merge_summaries()  — final topic-wise merge

│                 │     • answer_question()  — document-grounded Q&A

└────────┬────────┘

│

▼

┌─────────────────┐

│    app.py       │  ← Streamlit UI: Summary tab | Chat Q&A tab

└─────────────────┘

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- A [Google Gemini API key](https://ai.google.dev) (free tier works)
- Tesseract OCR (for scanned PDFs)

### Install Tesseract (for OCR support)

**Windows:** Download installer from [UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki) — during install, check **Urdu** in the language list. Also install [Poppler for Windows](https://github.com/oschwartz10612/poppler-windows/releases) and add both to your system PATH.

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr tesseract-ocr-urd poppler-utils
```

**macOS:**
```bash
brew install tesseract tesseract-lang poppler
```

### Installation

```bash
# 1. Clone the repo
git clone https://github.com/syedibrahimdev/Urdu-PDF-Summarizer-Q-A-Chatbot.git
cd Urdu-PDF-Summarizer-Q-A-Chatbot

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up environment variables
cp .env.example .env
# Add your Gemini API key inside .env:
# GEMINI_API_KEY=your_key_here

# 4. Run the app
streamlit run app.py
```

### `.env.example
GEMINI_API_KEY=your_gemini_api_key_here

---

## 📁 Project Structure
Urdu-PDF-Summarizer-Q-A-Chatbot/

│

├── app.py                  # Streamlit UI — main entry point

├── requirements.txt        # Python dependencies

├── packages.txt            # System dependencies (Tesseract, Poppler) for Streamlit Cloud

├── .env.example            # Environment variable template

├── .gitignore

│

└── src/

├── ingestion.py        # PDF extraction with smart OCR fallback

├── preprocessing.py    # Text cleaning & Urdu normalization

├── safe_text_utils.py  # Empty text validation, chunking, truncation

└── summarizer.py       # Gemini API: summarize + Q&A

---

## 🖥️ How to Use

1. **Upload** one or more Urdu/bilingual PDFs using the sidebar uploader
2. Click **فائلیں پروسیس کریں** — text is extracted (OCR runs automatically on scanned pages)
3. Go to the **خلاصہ (Summary)** tab → click **خلاصہ بنائیں**
4. Or go to the **سوال جواب (Chat)** tab → type your question in Urdu and get a grounded answer

---

## 🔧 Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.10+ |
| UI | Streamlit |
| PDF Parsing | pdfplumber |
| OCR | Tesseract 5.x (urd+eng) + pdf2image + Poppler |
| Text Cleaning | clean-text, regex |
| LLM | Google Gemini 2.5 Flash Lite |
| Config | python-dotenv |

---

## 🗺️ Roadmap

- [x] Single PDF upload & summarization
- [x] Urdu Q&A grounded in document
- [x] Multi-PDF support
- [x] Chat history with session state
- [x] Smart OCR fallback for scanned/image PDFs
- [x] RTL text rendering
- [x] Hosted deployment (Streamlit Cloud)
- [ ] Voice input (speech-to-text)
- [ ] Export summary as PDF

---

## 🤝 Contributing

Pull requests are welcome. For major changes, open an issue first to discuss what you'd like to change.

---

## 👨‍💻 Author

**Syed Ibrahim Ahmed**
[![GitHub](https://img.shields.io/badge/GitHub-syedibrahimdev-181717?style=flat&logo=github)](https://github.com/syedibrahimdev)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=flat&logo=linkedin)](https://linkedin.com/in/syedibrahimdev)

---

<div align="center">
  <sub>Built with ❤️ for the Urdu-speaking world</sub>
</div>