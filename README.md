# 📄 AI Agentic RAG System

<p align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google-Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-VectorDB-success?style=for-the-badge)
![Pinecone](https://img.shields.io/badge/Pinecone-Cloud-blueviolet?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)

</p>

---

# 📄 AI Agentic RAG System

<p align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google-Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-VectorDB-success?style=for-the-badge)
![Pinecone](https://img.shields.io/badge/Pinecone-Cloud-blueviolet?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)

</p>

---

# AI Agentic RAG System

An intelligent **Retrieval-Augmented Generation (RAG)** application powered by **Google Gemini**, **Sentence Transformers**, and **Vector Databases (ChromaDB/Pinecone)**. The system enables users to upload PDF documents, perform semantic search, and receive accurate, context-aware responses through specialized AI agents.

---

# 🏗️ System Architecture

<p align="center">
<img src="assets/architecture.png" width="100%">
</p>

---

# ✨ Features

- 📄 Upload and process PDF documents
- 🔍 Semantic document search
- 🤖 Intelligent AI Agent Routing
- 🧠 Google Gemini powered responses
- 🏢 Multi-company document management
- ☁️ ChromaDB (Local Storage)
- ☁️ Pinecone (Cloud Persistent Storage)
- 📚 Source Citations
- ⚡ Multi-Agent Comparison
- 🎨 Interactive Streamlit Dashboard

---

# 🤖 AI Agents

## 🛠️ Automation Agent

Generates:

- Python code
- Workflows
- Emails
- Step-by-step plans

---

## 🔍 Extraction Agent

Extracts:

- Dates
- Numbers
- Email addresses
- Phone numbers
- Invoice details
- Important facts

---

## 📊 Analytics Agent

Provides:

- Trend Analysis
- Data Insights
- Comparisons
- Summaries

---

## 💬 General RAG

Answers general document questions using retrieved context and Google Gemini.

---

# 🔄 Workflow

```text
Upload PDF
      │
      ▼
Document Loader
      │
      ▼
Text Chunking
      │
      ▼
Sentence Transformer
      │
      ▼
Vector Database
      │
      ▼
Semantic Retrieval
      │
      ▼
Retrieved Context
      │
      ▼
Agent Router
      │
 ┌────┼───────────────┐
 ▼    ▼               ▼
Automation    Extraction   Analytics
        │
        ▼
Google Gemini
        │
        ▼
Final Answer + Citations
```

---

# 📂 Project Structure

```text
AI-Agentic-RAG/
│
├── assets/
│   └── architecture.png
│
├── data/
│   ├── uploads/
│   └── chroma_db/
│
├── agents.py
├── config.py
├── document_loader.py
├── gemini_client.py
├── main.py
├── rag_engine.py
├── vector_store.py
├── requirements.txt
├── .gitignore
├── README.md
└── LICENSE
```

---

# ⚙️ Tech Stack

| Technology | Purpose |
|------------|----------|
| Python | Backend |
| Streamlit | Web UI |
| Google Gemini | Large Language Model |
| Sentence Transformers | Embeddings |
| ChromaDB | Local Vector Database |
| Pinecone | Cloud Vector Database |
| PyPDF | PDF Processing |
| python-dotenv | Environment Variables |

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/yourusername/AI-Agentic-RAG.git

cd AI-Agentic-RAG
```
An intelligent **Retrieval-Augmented Generation (RAG)** application powered by **Google Gemini**, **Sentence Transformers**, and **Vector Databases (ChromaDB/Pinecone)**. The system enables users to upload PDF documents, perform semantic search, and receive accurate, context-aware responses through specialized AI agents.

---

# 🏗️ System Architecture

<p align="center">
<img src="assets/architecture.png" width="100%">
</p>

---

# ✨ Features

- 📄 Upload and process PDF documents
- 🔍 Semantic document search
- 🤖 Intelligent AI Agent Routing
- 🧠 Google Gemini powered responses
- 🏢 Multi-company document management
- ☁️ ChromaDB (Local Storage)
- ☁️ Pinecone (Cloud Persistent Storage)
- 📚 Source Citations
- ⚡ Multi-Agent Comparison
- 🎨 Interactive Streamlit Dashboard

---

# 🤖 AI Agents

## 🛠️ Automation Agent

Generates:

- Python code
- Workflows
- Emails
- Step-by-step plans

---

## 🔍 Extraction Agent

Extracts:

- Dates
- Numbers
- Email addresses
- Phone numbers
- Invoice details
- Important facts

---

## 📊 Analytics Agent

Provides:

- Trend Analysis
- Data Insights
- Comparisons
- Summaries

---

## 💬 General RAG

Answers general document questions using retrieved context and Google Gemini.

---

# 🔄 Workflow

```text
Upload PDF
      │
      ▼
Document Loader
      │
      ▼
Text Chunking
      │
      ▼
Sentence Transformer
      │
      ▼
Vector Database
      │
      ▼
Semantic Retrieval
      │
      ▼
Retrieved Context
      │
      ▼
Agent Router
      │
 ┌────┼───────────────┐
 ▼    ▼               ▼
Automation    Extraction   Analytics
        │
        ▼
Google Gemini
        │
        ▼
Final Answer + Citations
```

---

# 📂 Project Structure

```text
AI-Agentic-RAG/
│
├── assets/
│   └── architecture.png
│
├── data/
│   ├── uploads/
│   └── chroma_db/
│
├── agents.py
├── config.py
├── document_loader.py
├── gemini_client.py
├── main.py
├── rag_engine.py
├── vector_store.py
├── requirements.txt
├── .gitignore
├── README.md
└── LICENSE
```

---

# ⚙️ Tech Stack

| Technology | Purpose |
|------------|----------|
| Python | Backend |
| Streamlit | Web UI |
| Google Gemini | Large Language Model |
| Sentence Transformers | Embeddings |
| ChromaDB | Local Vector Database |
| Pinecone | Cloud Vector Database |
| PyPDF | PDF Processing |
| python-dotenv | Environment Variables |

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/yourusername/AI-Agentic-RAG.git

cd AI-Agentic-RAG
```

Install dependencies

```bash
pip install -r requirements.txt
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

# 📚 RAG Pipeline

1. Upload PDF
2. Extract Text
3. Chunk Text
4. Generate Embeddings
5. Store in Vector Database
6. Retrieve Relevant Chunks
7. Route Question to Appropriate Agent
8. Generate Response using Gemini
9. Return Final Answer with Citations

---

# 🏢 Multi-Company Support

Each uploaded PDF is associated with a company namespace.

Example:

- Google
- Microsoft
- Amazon
- Tesla

Users can search:

- Across all companies
- Within a single company

---

# 📸 Screenshots

## Home Page

> Add screenshot here

```
screenshots/home.png
```

## Upload Documents

> Add screenshot here

```
screenshots/upload.png
```

## Ask Questions

> Add screenshot here

```
screenshots/chat.png
```

## Multi-Agent Comparison

> Add screenshot here

```
screenshots/compare.png
```

---

# 🔮 Future Improvements

- Hybrid Search (BM25 + Vector Search)
- Cross Encoder Re-ranking
- LangChain Integration
- Semantic Chunking
- OCR Support
- Conversation Memory
- Multi-modal RAG
- Tool Calling Agents
- Async Agent Execution
- Document Versioning

---

# 👩‍💻 Author

**Mahnoor Hassan**

Artificial Intelligence Undergraduate

### Skills

- Python
- Machine Learning
- Artificial Intelligence
- Retrieval-Augmented Generation (RAG)
- Agentic AI
- Google Gemini
- Streamlit
- Pinecone
- ChromaDB

---

# 📄 License

This project is licensed under the **MIT License**.

---

<p align="center">

⭐ If you found this project useful, please consider giving it a **Star**.

</p>