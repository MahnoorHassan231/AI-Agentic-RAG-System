# AI Agentic RAG System

PDF documents par sawal poochne wala RAG system, jo Gemini + ChromaDB + AI Agents (Automation, Extraction, Analytics) use karta hai.

## Architecture

```
User → Streamlit UI → RAG Engine → Document Loader → Chunking →
SentenceTransformer (Embeddings) → ChromaDB (Vector Store) →
Similarity Search → AI Agent Router → Gemini → Answer
```

## Setup (apne computer par)

1. **Python 3.10+ install hona chahiye**

2. **Virtual environment banayein (optional but recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```

3. **Dependencies install karein**
   ```bash
   pip install -r requirements.txt
   ```

4. **Gemini API Key set karein**
   - Google AI Studio (https://aistudio.google.com/apikey) se free API key lein
   - `.env.example` ko `.env` mein rename karein
   - Usmein apni key daal dein:
     ```
     GEMINI_API_KEY=your_actual_key_here
     ```

5. **App run karein**
   ```bash
   streamlit run main.py
   ```

6. Browser mein `http://localhost:8501` khul jayega.

## Files ka kaam (short summary)

| File | Kaam |
|---|---|
| `config.py` | Settings, API key, folder paths |
| `gemini_client.py` | Sirf Gemini se baat karta hai |
| `document_loader.py` | PDF read + chunking |
| `vector_store.py` | Embeddings + ChromaDB |
| `agents.py` | 3 AI Agents (Automation, Extraction, Analytics) + Router |
| `rag_engine.py` | Sab files ko connect karta hai (project ka brain) |
| `main.py` | Streamlit UI |

## Use kaise karein

1. Sidebar se apni PDF(s) upload karein aur "Process PDFs" click karein.
2. Neeche textbox mein sawal likhein, e.g.: *"How many annual leaves do employees get?"*
3. "Ask" click karein — answer, kaunsa agent use hua, aur retrieved context sab dikhega.

## Interview ke liye one-liner

> RAG (Retrieval-Augmented Generation) mein pehle user ke question ke mutabiq vector database se relevant chunks retrieve kiye jate hain, phir sirf wahi context LLM ko diya jata hai — isse answer accurate hota hai aur hallucination kam hoti hai.
