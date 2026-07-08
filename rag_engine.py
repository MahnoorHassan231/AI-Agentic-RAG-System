"""
rag_engine.py
-------------
The BRAIN of the project. Connects all the pieces together:

document_loader -> vector_store -> agents -> gemini_client

Flow:
1. PDF upload      -> load + chunk + embed + store
2. User question    -> embed -> search -> relevant context + sources retrieved
3. Router decides which agent(s) should run (via LLM-based classification)
4. Agent(s) generate the final answer(s) via Gemini
"""

import os
import config
from document_loader import load_and_chunk_pdf
from vector_store import VectorStore
from gemini_client import GeminiClient
from agents import AgentRouter


class RAGEngine:
    def __init__(self):
        self.vector_store = VectorStore()
        self.gemini = GeminiClient()
        self.router = AgentRouter(self.gemini)

    def ingest_pdf(self, pdf_path: str) -> int:
        """
        Processes a new PDF: read -> chunk -> embed -> save to ChromaDB.
        Returns how many chunks were saved.
        """
        chunks = load_and_chunk_pdf(pdf_path)
        source_name = os.path.basename(pdf_path)
        self.vector_store.add_chunks(chunks, source_name)
        return len(chunks)

    def _get_context_and_sources(self, question: str) -> tuple[str, list[str]]:
        """
        Retrieves relevant chunks AND tracks which PDF each one came from.
        Returns (context_text, list_of_unique_source_filenames).
        """
        results = self.vector_store.search_with_sources(question)
        context = "\n\n".join(r["text"] for r in results)
        sources = sorted(set(r["source"] for r in results))
        return context, sources

    def ask(self, question: str, use_llm_routing: bool = True) -> dict:
        """
        Single-agent mode (default): picks ONE best-fit agent and returns its answer.

        use_llm_routing=True  -> Gemini itself decides which agent fits best (more accurate)
        use_llm_routing=False -> fast keyword-based routing (no extra LLM call)
        """
        if not self.vector_store.has_documents():
            return {
                "answer": "Please upload a PDF first, then ask your question.",
                "agent_used": "none",
                "context_used": "",
                "sources": [],
            }

        context, sources = self._get_context_and_sources(question)

        if use_llm_routing:
            agent_type = self.router.classify_with_llm(question)
        else:
            agent_type = self.router.route(question)

        answer = self.router.run_agent(agent_type, context, question)

        return {
            "answer": answer,
            "agent_used": agent_type,
            "context_used": context,
            "sources": sources,
        }

    def ask_multi(self, question: str, run_all: bool = False) -> dict:
        """
        Multi-agent mode: returns answers from MULTIPLE agents so they can
        be compared side-by-side.

        run_all=False -> only agents whose keywords matched the question run
        run_all=True  -> all 3 agents + General RAG answer run, always
        """
        if not self.vector_store.has_documents():
            return {
                "answers": {"General": "Please upload a PDF first, then ask your question."},
                "context_used": "",
                "sources": [],
            }

        context, sources = self._get_context_and_sources(question)

        if run_all:
            answers = self.router.run_all_agents(context, question)
        else:
            answers = self.router.run_matching_agents(context, question)

        return {
            "answers": answers,
            "context_used": context,
            "sources": sources,
        }