"""
config.py
---------
Central configuration: API keys, model names, folder paths.
No logic here — just values.

Works in TWO environments automatically:
1. Local machine   -> reads keys from the .env file
2. Streamlit Cloud -> reads keys from st.secrets (Settings -> Secrets)
"""

import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Pinecone (OPTIONAL) - if set, enables PERMANENT cloud storage.
# If left empty, the app falls back to local ChromaDB (session-only storage).
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "ai-rag-project")

# Fall back to Streamlit Cloud secrets if not found locally
if not GEMINI_API_KEY or not PINECONE_API_KEY:
    try:
        import streamlit as st
        if not GEMINI_API_KEY:
            GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
        if not PINECONE_API_KEY:
            PINECONE_API_KEY = st.secrets.get("PINECONE_API_KEY", "")
            PINECONE_INDEX_NAME = st.secrets.get("PINECONE_INDEX_NAME", PINECONE_INDEX_NAME)
    except Exception:
        pass

GEMINI_MODEL = "gemini-2.5-flash"

UPLOAD_DIR = "data/uploads"
CHROMA_DIR = "data/chroma_db"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

CHUNK_SIZE = 500        # characters per chunk
CHUNK_OVERLAP = 50      # overlap so context isn't lost between chunks

TOP_K_RESULTS = 3        # how many relevant chunks to retrieve per query

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(CHROMA_DIR, exist_ok=True)