"""
vector_store.py
----------------
Handles two things:
1. Converting text into embeddings (numbers/vectors) -> SentenceTransformer
2. Storing and searching those vectors

Supports TWO backends automatically:
- ChromaDB (default) -> stores data on local disk. Great for local testing,
  but data is LOST whenever the app container restarts (e.g. on Streamlit Cloud).
- Pinecone (if PINECONE_API_KEY is set) -> stores data on Pinecone's cloud
  servers. Data PERSISTS permanently, independent of the app restarting.

Each "company" is stored in its own Pinecone namespace, which also gives us
an easy way to list all companies and to filter searches to just one company.
"""

import chromadb
from sentence_transformers import SentenceTransformer
import config


def _sanitize_namespace(name: str) -> str:
    """Pinecone namespaces must be simple strings; keep it safe & consistent."""
    return name.strip().lower().replace(" ", "_")


class VectorStore:
    def __init__(self):
        # Embedding model (text -> numbers). Same for both backends.
        self.embedder = SentenceTransformer(config.EMBEDDING_MODEL)

        self.use_pinecone = bool(config.PINECONE_API_KEY)

        if self.use_pinecone:
            self._init_pinecone()
        else:
            self._init_chroma()

    # ------------------------------------------------------------------
    # Backend initialization
    # ------------------------------------------------------------------

    def _init_chroma(self):
        self.client = chromadb.PersistentClient(path=config.CHROMA_DIR)
        self.collection = self.client.get_or_create_collection(name="documents")

    def _init_pinecone(self):
        from pinecone import Pinecone, ServerlessSpec

        pc = Pinecone(api_key=config.PINECONE_API_KEY)
        index_name = config.PINECONE_INDEX_NAME
        embedding_dim = self.embedder.get_sentence_embedding_dimension()

        existing = [i["name"] for i in pc.list_indexes()]
        if index_name not in existing:
            pc.create_index(
                name=index_name,
                dimension=embedding_dim,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1"),
            )
        self.index = pc.Index(index_name)

    # ------------------------------------------------------------------
    # Adding documents
    # ------------------------------------------------------------------

    def add_chunks(self, chunks: list[str], source_name: str, company: str = None):
        """
        Converts chunks to embeddings and saves them, tagged with which
        PDF (source) and which company they came from.
        """
        if not chunks:
            return

        company = company or source_name
        embeddings = self.embedder.encode(chunks).tolist()
        ids = [f"{source_name}_{i}" for i in range(len(chunks))]

        if self.use_pinecone:
            namespace = _sanitize_namespace(company)
            vectors = [
                (ids[i], embeddings[i], {"source": source_name, "company": company, "text": chunks[i]})
                for i in range(len(chunks))
            ]
            self.index.upsert(vectors=vectors, namespace=namespace)
        else:
            metadatas = [{"source": source_name, "company": company} for _ in chunks]
            self.collection.add(documents=chunks, embeddings=embeddings, ids=ids, metadatas=metadatas)

    # ------------------------------------------------------------------
    # Searching
    # ------------------------------------------------------------------

    def search(self, query: str, top_k: int = None) -> list[str]:
        """Backwards-compatible: plain text chunks only, no company filter."""
        results = self.search_with_sources(query, top_k)
        return [r["text"] for r in results]

    def search_with_sources(self, query: str, top_k: int = None, company: str = None) -> list[dict]:
        """
        Finds the most relevant chunks for a question.
        If 'company' is given, only searches within that company's documents.
        Returns: [{"text": ..., "source": ..., "company": ...}, ...]
        """
        top_k = top_k or config.TOP_K_RESULTS
        query_embedding = self.embedder.encode([query]).tolist()[0]

        if self.use_pinecone:
            return self._search_pinecone(query_embedding, top_k, company)
        else:
            return self._search_chroma(query_embedding, top_k, company)

    def _search_chroma(self, query_embedding, top_k, company):
        query_kwargs = {"query_embeddings": [query_embedding], "n_results": top_k}
        if company:
            query_kwargs["where"] = {"company": company}

        results = self.collection.query(**query_kwargs)
        documents = results.get("documents", [[]])
        metadatas = results.get("metadatas", [[]])
        documents = documents[0] if documents else []
        metadatas = metadatas[0] if metadatas else []

        combined = []
        for i, doc in enumerate(documents):
            meta = metadatas[i] if i < len(metadatas) else {}
            combined.append({
                "text": doc,
                "source": meta.get("source", "unknown"),
                "company": meta.get("company", "unknown"),
            })
        return combined

    def _search_pinecone(self, query_embedding, top_k, company):
        if company:
            namespaces = [_sanitize_namespace(company)]
        else:
            stats = self.index.describe_index_stats()
            namespaces = list(stats.get("namespaces", {}).keys())

        all_matches = []
        for ns in namespaces:
            try:
                res = self.index.query(
                    vector=query_embedding, top_k=top_k, namespace=ns, include_metadata=True
                )
                all_matches.extend(res.matches)
            except Exception:
                continue

        # If searching across all companies, merge + keep the overall best matches
        all_matches.sort(key=lambda m: m.score, reverse=True)
        all_matches = all_matches[:top_k]

        combined = []
        for m in all_matches:
            meta = m.metadata or {}
            combined.append({
                "text": meta.get("text", ""),
                "source": meta.get("source", "unknown"),
                "company": meta.get("company", "unknown"),
            })
        return combined

    # ------------------------------------------------------------------
    # Metadata helpers
    # ------------------------------------------------------------------

    def get_all_companies(self) -> list[str]:
        """Returns a sorted list of all distinct company names currently stored."""
        if self.use_pinecone:
            stats = self.index.describe_index_stats()
            namespaces = stats.get("namespaces", {})
            # namespace names are sanitized (lowercase/underscored); we don't have
            # the original casing here, so we display the namespace as-is.
            return sorted(ns for ns in namespaces.keys() if ns)
        else:
            if self.collection.count() == 0:
                return []
            all_data = self.collection.get(include=["metadatas"])
            companies = {m.get("company", "unknown") for m in all_data["metadatas"]}
            return sorted(companies)

    def has_documents(self) -> bool:
        if self.use_pinecone:
            stats = self.index.describe_index_stats()
            return stats.get("total_vector_count", 0) > 0
        else:
            return self.collection.count() > 0

    @property
    def backend_name(self) -> str:
        return "Pinecone (permanent cloud)" if self.use_pinecone else "ChromaDB (local, session-only)"