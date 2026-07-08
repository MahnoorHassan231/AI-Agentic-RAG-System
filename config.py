"""
config.py
---------
Sab settings yahan hain: API key, model name, folder paths.
Iska kaam sirf values dena hai — koi logic nahi.
"""

import os
from dotenv import load_dotenv

# .env file se environment variables load karo
load_dotenv()

# Gemini API Key (.env file mein GEMINI_API_KEY=xxxx daalna)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Gemini model jo use hoga
GEMINI_MODEL = "gemini-2.5-flash"

# Folder jahan uploaded PDFs save hongi
UPLOAD_DIR = "data/uploads"

# ChromaDB ka persistent storage folder
CHROMA_DIR = "data/chroma_db"

# Embedding model (SentenceTransformer)
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Chunking settings
CHUNK_SIZE = 500        # characters per chunk
CHUNK_OVERLAP = 50      # overlap taake context na tootay

# Kitne relevant chunks retrieve karne hain
TOP_K_RESULTS = 3

# Folders create karo agar exist nahi karte
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(CHROMA_DIR, exist_ok=True)
