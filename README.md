# 🤖 AI Agentic RAG System

An intelligent **Multi-Agent Retrieval-Augmented Generation (RAG)** system built with **Python, Streamlit, Gemini AI, ChromaDB, and Pinecone**.

This project allows users to upload PDF documents, retrieve relevant information using semantic search, and generate accurate AI-powered answers using multiple specialized AI agents.

---

## 📌 Features

- 📄 Upload and process PDF documents
- ✂️ Automatic document chunking
- 🧠 Semantic search using Sentence Transformers
- 🤖 Gemini 2.5 Flash integration
- 🗂️ ChromaDB support for local vector storage
- ☁️ Pinecone support for permanent cloud vector storage
- 🏢 Multi-company document management
- 🎯 AI Agent Routing
- 📊 Multi-Agent comparison mode
- 📚 Source citation support
- 💬 Interactive Streamlit interface

---

# 🏗️ System Architecture

<p align="center">
    <img src="architecture-diagram.png" alt="System Architecture" width="100%">
</p>

---

## 🔄 System Workflow

```
User
   │
   ▼
Upload PDF
   │
   ▼
Document Loader
   │
   ▼
Text Chunking
   │
   ▼
Sentence Transformer Embeddings
   │
   ▼
Vector Database
(ChromaDB / Pinecone)
   │
   ▼
User Question
   │
   ▼
Semantic Search
   │
   ▼
Relevant Context Retrieval
   │
   ▼
LLM Agent Router
   │
   ▼
┌───────────────┬───────────────┬───────────────┐
│ Automation    │ Extraction    │ Analytics     │
│ Agent         │ Agent         │ Agent         │
└───────────────┴───────────────┴───────────────┘
                │
                ▼
          Gemini 2.5 Flash
                │
                ▼
          Final AI Response
```

---

# 📂 Project Structure

```
AI-Agentic-RAG-System
│
├── agents.py
├── config.py
├── document_loader.py
├── gemini_client.py
├── rag_engine.py
├── vector_store.py
├── main.py
├── requirements.txt
├── architecture-diagram.png
├── README.md
└── .gitignore
```

---

# 🧠 AI Agents

## 🤖 Automation Agent

Responsible for:

- Workflow generation
- Code generation
- Email generation
- Step-by-step plans

---

## 📑 Extraction Agent

Responsible for:

- Extracting dates
- Invoice information
- Phone numbers
- Email addresses
- Numerical values

---

## 📈 Analytics Agent

Responsible for:

- Data analysis
- Trend analysis
- Summaries
- Insights
- Comparisons

---

# ⚙️ Technologies Used

- Python
- Streamlit
- Google Gemini 2.5 Flash
- ChromaDB
- Pinecone
- Sentence Transformers
- PyPDF
- Python Dotenv

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/MahnoorHassan231/AI-Agentic-RAG-System.git
```

Move into the project

```bash
cd AI-Agentic-RAG-System
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
PINECONE_API_KEY=YOUR_PINECONE_API_KEY
PINECONE_INDEX_NAME=ai-rag-project
```

Run the application

```bash
streamlit run main.py
```

---

# 📖 How It Works

1. Upload one or more PDF documents.
2. Documents are converted into text.
3. Text is split into chunks.
4. Chunks are converted into embeddings.
5. Embeddings are stored in ChromaDB or Pinecone.
6. User asks a question.
7. Semantic search retrieves the most relevant chunks.
8. Agent Router selects the appropriate AI agent.
9. Gemini generates the final answer.
10. Sources are displayed with the response.

---

# 🎯 Future Improvements

- OCR support
- Image understanding
- Voice interaction
- Web document ingestion
- Hybrid search
- Conversation memory
- Authentication
- Docker deployment
- Azure & AWS deployment

---

# 👩‍💻 Author

**Mahnoor Hassan**

AI Student | Python Developer | AI & Machine Learning Enthusiast

GitHub:
https://github.com/MahnoorHassan231

---

# ⭐ If you found this project useful, don't forget to star the repository!
