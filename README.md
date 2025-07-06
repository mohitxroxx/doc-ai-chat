# Chat with PDFs using LLaMA 3 (Ollama + LangChain)

This is an AI-powered app that lets you **upload PDFs** and **chat with them** using the **LLaMA 3.1:8B model** via **Ollama**, powered by LangChain and FAISS.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/mohitxroxx/doc-ai-chat
cd doc-ai-chat
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Pull LLaMA 3 with Ollama

```bash
ollama pull llama3.1:8B
```

Make sure Ollama is running:
```bash
ollama run llama3.1:8B
```

---

## Running the App

### 1. Start the FastAPI backend

```bash
uvicorn main:app --reload
```

> Runs at: `http://localhost:8000/docs` for API testing

### 2. Start the Streamlit frontend

```bash
streamlit run app.py
```

> Runs at: `http://localhost:8501` for user interface

---
