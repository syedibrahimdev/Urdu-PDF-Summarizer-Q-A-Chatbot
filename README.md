<div align="center">

# 📚 Urdu PDF Summarizer & Q&A Chatbot

**AI-powered Urdu document assistant — upload any PDF, get a structured Urdu summary or ask questions in Urdu.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Gemini](https://img.shields.io/badge/Google%20Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

[🚀 Live Demo](#) · [📂 Source Code](https://github.com/syedibrahimdev/Urdu-PDF-Summarizer-Q-A-Chatbot) · [🐛 Report Bug](https://github.com/syedibrahimdev/Urdu-PDF-Summarizer-Q-A-Chatbot/issues)

</div>

---

## 🧐 What Is This?

Most AI tools fail at Urdu — they either transliterate badly or ignore the language entirely.

**Urdu PDF Summarizer** fixes that. Upload any Urdu or bilingual PDF and the app will:
- Extract and clean the Urdu text properly (preserving RTL characters)
- Generate a **structured, topic-wise Urdu summary** using Google Gemini
- Let you **ask questions in Urdu** and get answers grounded in the document

Built for students, researchers, and professionals who work with Urdu content.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📄 PDF Text Extraction | Extracts Urdu/bilingual text using `pdfplumber` |
| 🧹 Urdu Text Normalization | Cleans unicode artifacts, extra spaces, broken line breaks |
| 📝 Structured Summarization | Chunk-based summarization merged into topic-wise headings |
| ❓ Document Q&A | Ask any question — answers are grounded in the uploaded PDF only |
| ⚡ Streamlit UI | Simple, tabbed interface — no technical knowledge needed |

---

## 🏗️ Architecture

```
📂 Upload PDF
      │
      ▼
┌─────────────────┐
│   ingestion.py  │  ← pdfplumber extracts raw text page by page
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
│  summarizer.py  │  ← Gemini 1.5 Flash
│                 │     • summarize_chunk()  — per-chunk Urdu summary
│                 │     • merge_summaries()  — final topic-wise merge
│                 │     • answer_question()  — document-grounded Q&A
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    app.py       │  ← Streamlit UI with two tabs: Summary | Q&A
└─────────────────┘
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- A [Google Gemini API key](https://ai.google.dev) (free tier works)

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

### `.env.example`
```
GEMINI_API_KEY=your_gemini_api_key_here
```

---

## 📁 Project Structure

```
Urdu-PDF-Summarizer-Q-A-Chatbot/
│
├── app.py                  # Streamlit UI — main entry point
├── requirements.txt        # All dependencies
├── .env.example            # Environment variable template
├── .gitignore
│
└── src/
    ├── ingestion.py        # PDF text extraction (pdfplumber)
    ├── preprocessing.py    # Text cleaning & Urdu normalization
    ├── safe_text_utils.py  # Empty text validation, chunking
    └── summarizer.py       # Gemini API: summarize + Q&A
```

---

## 🖥️ How to Use

1. **Upload** any Urdu or bilingual PDF using the file uploader
2. Wait for text extraction and normalization
3. Go to the **خلاصہ (Summary)** tab → click **خلاصہ بنائیں**
4. Or go to **سوال جواب (Q&A)** tab → type your question → click **جواب حاصل کریں**

---

## 🔧 Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.10+ |
| UI | Streamlit |
| PDF Parsing | pdfplumber |
| Text Cleaning | clean-text, regex |
| LLM | Google Gemini 1.5 Flash |
| Config | python-dotenv |

---

## 🗺️ Roadmap

- [x] Single PDF upload & summarization
- [x] Urdu Q&A grounded in document
- [ ] Multi-PDF support
- [ ] Chat history with memory
- [ ] Voice input (speech-to-text)
- [ ] Hosted deployment (Streamlit Cloud)

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
