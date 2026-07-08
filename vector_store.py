"""
vector_store.py
----------------
Iska kaam hai:
1. Text ko embedding (numbers/vector) mein badalna  -> SentenceTransformer
2. Un vectors ko save aur search karna              -> ChromaDB
"""

import chromadb
from sentence_transformers import SentenceTransformer
import config


class VectorStore:
    def __init__(self):
        # Embedding model load karo (text -> numbers)
        self.embedder = SentenceTransformer(config.EMBEDDING_MODEL)

        # ChromaDB client (disk par persist hoga, restart ke baad bhi data rahega)
        self.client = chromadb.PersistentClient(path=config.CHROMA_DIR)
        self.collection = self.client.get_or_create_collection(name="documents")

    def add_chunks(self, chunks: list[str], source_name: str):
        """
        Chunks ko embedding mein convert karke ChromaDB mein save karta hai.
        Har chunk ka ek unique id banaya jata hai.
        """
        if not chunks:
            return

        embeddings = self.embedder.encode(chunks).tolist()
        ids = [f"{source_name}_{i}" for i in range(len(chunks))]
        metadatas = [{"source": source_name} for _ in chunks]

        self.collection.add(
            documents=chunks,
            embeddings=embeddings,
            ids=ids,
            metadatas=metadatas,
        )

    def search(self, query: str, top_k: int = None) -> list[str]:
        """
        Question ko bhi embedding mein badalta hai, phir ChromaDB mein
        sabse similar (matlab sabse relevant) chunks dhoondta hai.
        Kept for backwards-compatibility — returns plain text chunks only.
        """
        results = self.search_with_sources(query, top_k)
        return [r["text"] for r in results]

    def search_with_sources(self, query: str, top_k: int = None) -> list[dict]:
        """
        Same as search(), but also returns WHICH PDF each chunk came from,
        so answers can be traced back to a source document (citations).
        Returns: [{"text": "...", "source": "handbook.pdf"}, ...]
        """
        top_k = top_k or config.TOP_K_RESULTS
        query_embedding = self.embedder.encode([query]).tolist()

        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=top_k,
        )

        documents = results.get("documents", [[]])
        metadatas = results.get("metadatas", [[]])
        documents = documents[0] if documents else []
        metadatas = metadatas[0] if metadatas else []

        combined = []
        for i, doc in enumerate(documents):
            source = metadatas[i].get("source", "unknown") if i < len(metadatas) else "unknown"
            combined.append({"text": doc, "source": source})
        return combined

    def has_documents(self) -> bool:
        return self.collection.count() > 0