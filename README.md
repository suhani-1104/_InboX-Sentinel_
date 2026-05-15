# 🤖 InboxSentinel (Spam-V-Ham)

InboxSentinel is a full-stack, Agentic AI-Based Email Spam Detection and Intelligent Filtering System. It leverages state-of-the-art Natural Language Processing (NLP) to autonomously scan, classify, and explain decisions regarding incoming emails.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B)
![Flask](https://img.shields.io/badge/Flask-2.0%2B-000000)
![Transformers](https://img.shields.io/badge/HuggingFace-Transformers-F9AB00)

---

## ✨ Features

- **🧠 Agentic AI Pipeline**: Not just a classifier. The agent calculates probability, applies rule-based action thresholds (>80% Block, >50% Flag), and acts on the classification.
- **🔍 Explainable AI**: Automatically analyzes text heuristics to provide human-readable explanations for *why* an email was flagged.
- **⚡ Transformer-Powered**: Uses the highly efficient `mrm8488/bert-tiny-finetuned-sms-spam-detection` model from Hugging Face for lightning-fast inference.
- **🎨 Beautiful UI**: A unified single-page Streamlit dashboard featuring top-tab navigation and native light/dark mode toggling (`Soft Pastel Minimal` vs `Indigo Night`).
- **📊 Real-time Analytics**: Built-in interactive Plotly charts tracking spam distribution and agent confidence scores.

---

## 🏗️ Architecture

```text
c:/PROJECTS/EMAIL_CLASSIFIER/
├── backend/
│   ├── app.py                 # Flask API entry point
│   ├── agent.py               # Agent logic (classifier, decision engine, explainer)
│   └── email_service.py       # Mock email generation (SMS-style templates)
├── frontend/
│   ├── Home.py                # Main Streamlit application with Tabs
│   └── theme_utils.py         # Dynamic Light/Dark CSS injection
├── requirements.txt           # Project dependencies
└── run.py                     # Convenience runner script
```

---

## 🚀 Getting Started

### 1. Prerequisites
Make sure you have Python 3.8+ installed.

### 2. Installation
Clone the repository and install the required dependencies:

```bash
git clone https://github.com/suhani-1104/_InboX-Sentinel_.git
cd _InboX-Sentinel_
pip install -r requirements.txt
```

### 3. Running the System
The project includes a convenience script that automatically boots both the Flask API backend and the Streamlit frontend.

```bash
python run.py
```

- The Streamlit Dashboard will open automatically in your browser at `http://localhost:8501`.
- The Flask backend will run silently on `http://localhost:5000`.

> **Note:** The first time you launch the application and click "Scan Emails Now", it will take a few seconds as the Hugging Face `transformers` pipeline downloads the model weights to your local cache. Subsequent scans are instantaneous!

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit, HTML/CSS
- **Backend**: Python, Flask, Flask-CORS
- **Machine Learning**: Hugging Face Transformers (`pipeline`), PyTorch
- **Data Visualization**: Plotly Express, Pandas

---

## 🔮 Future Enhancements
- **Gmail API Integration**: Swap the `MockEmailService` for OAuth 2.0 real-time Gmail fetching.
- **Multi-Agent Architecture**: Add dedicated agents for phishing link detection and sender reputation scoring.
- **RAG-based Reasoning**: Provide deep contextual explanations by comparing incoming emails to historical inbox patterns.