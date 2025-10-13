# 📚 StudyBuddy – Urdu PDF Summarizer & Q&A Chatbot

StudyBuddy is an AI-powered *Urdu document assistant* that helps users upload PDFs and either *summarize them in Urdu* or *ask context-based questions* directly from the content — powered by *Google Gemini AI*.

---

## 🚀 Features

- 📂 Upload Urdu or bilingual PDFs  
- 🧠 AI-powered Urdu summarization  
- ❓ Question-answering from PDF context  
- 🔤 Cleans, normalizes, and processes Urdu text for better understanding  
- ⚡ Built with Streamlit for instant web app experience

---

## 🧰 Tech Stack

- *Frontend & UI:* Streamlit  
- *Backend:* Python  
- *AI Model:* Google Gemini (via google-generativeai)  
- *Text Processing:* pdfplumber, clean-text, regex  
- *Environment:* dotenv, venv  

---

## 🗂️ Folder Structure

Urdu-PDF-Summarizer-Q-A-Chatbot/StudyBuddy/
│
├── 📄 app.py
│
├── 📄 requirements.txt
├── 📄 .gitignore
├── 📄 .env.example
│
├── 📁 src/
│   ├── _init_.py
│   ├── ingestion.py
│   ├── preprocessing.py
│   ├── safe_text_utils.py
│   └── summarizer.py
│
├── 📁 temp_uploaded/
│   └── (temporary PDF files go here, ignored by Git)
│
└── 📄 README.md

---

## ⚙️ Installation & Usage

### 1. Clone the Repository
bash
git clone https://github.com/syedibrahimdev/Urdu-PDF-Summarizer-Q-A-Chatbot.git

cd Urdu-PDF-Summarizer-Q-A-Chatbot

### 2. Create & Activate Virtual Environment

python -m venv venv
venv\Scripts\activate     # On Windows
source venv/bin/activate  # On Mac/Linux

### 3. Install Dependencies

pip install -r requirements.txt

### 4. Set Up Environment Variables

Create a .env file in the root directory and add your Gemini API key:

GEMINI_API_KEY=your_api_key_here

### 5. Run the App

streamlit run app.py


---

### 🔮 Future Improvements

🗣️ Add voice-based Urdu query input

🌍 Add multilingual support (Arabic, English)

🧩 Improve summarization coherence for large PDFs

☁️ Deploy on Streamlit Cloud or Hugging Face Spaces



---

### 👤 Author

Syed Ibrahim Ahmed
🎓 AI Engineer in Progress | Machine Learning & Data Science Enthusiast
📧 [ibooo786@hotmail.com]
🌐 [LinkedIn Profile](https://www.linkedin.com/in/syed-ibrahim-ahmed-6aa304247)


---

⭐ If you like this project, give it a star!
Your support motivates me to build better AI tools 🌟
