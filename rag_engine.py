"""
rag_engine.py
-------------
The BRAIN of the project. Connects all the pieces together:

document_loader -> vector_store -> agents -> gemini_client

Flow:
1. PDF upload      -> load + chunk + embed + store (tagged with a company name)
2. User question    -> embed -> search (optionally filtered by company) -> context + per-chunk sources
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

    def ingest_pdf(self, pdf_path: str, company: str = None) -> int:
        """
        Processes a new PDF: read -> chunk -> embed -> save,
        tagged with the given company/client name.
        Returns how many chunks were saved.
        """
        chunks = load_and_chunk_pdf(pdf_path)
        source_name = os.path.basename(pdf_path)
        self.vector_store.add_chunks(chunks, source_name, company=company)
        return len(chunks)

    def get_all_companies(self) -> list[str]:
        return self.vector_store.get_all_companies()

    def _get_context_and_citations(self, question: str, company: str = None) -> tuple[str, list[dict]]:
        """
        Retrieves relevant chunks AND tracks exactly which company + PDF
        each one came from. Each chunk in the context is tagged inline
        (e.g. "[Acme Corp - handbook.pdf]") so Gemini can reference the
        right source when multiple companies are being searched together.

        Returns:
          context_text -> the tagged context string sent to Gemini
          citations     -> [{"company": ..., "source": ...}, ...] (unique, in relevance order)
        """
        results = self.vector_store.search_with_sources(question, company=company)

        context_parts = []
        seen = set()
        citations = []
        for r in results:
            tag = f"[{r['company']} - {r['source']}]"
            context_parts.append(f"{tag}\n{r['text']}")

            key = (r["company"], r["source"])
            if key not in seen:
                seen.add(key)
                citations.append({"company": r["company"], "source": r["source"]})

        context = "\n\n".join(context_parts)
        return context, citations

    def ask(self, question: str, use_llm_routing: bool = True, company: str = None) -> dict:
        """
        Single-agent mode (default): picks ONE best-fit agent and returns its answer.

        company=None       -> searches across ALL uploaded companies' documents
        company="Acme Corp" -> searches ONLY within that company's documents
        """
        if not self.vector_store.has_documents():
            return {
                "answer": "Please upload a PDF first, then ask your question.",
                "agent_used": "none",
                "context_used": "",
                "citations": [],
            }

        context, citations = self._get_context_and_citations(question, company=company)

        if not context:
            return {
                "answer": "No matching documents found for this company/filter. "
                          "Try selecting 'All Companies' or upload a document for this company.",
                "agent_used": "none",
                "context_used": "",
                "citations": [],
            }

        if use_llm_routing:
            agent_type = self.router.classify_with_llm(question)
        else:
            agent_type = self.router.route(question)

        answer = self.router.run_agent(agent_type, context, question)

        return {
            "answer": answer,
            "agent_used": agent_type,
            "context_used": context,
            "citations": citations,
        }

    def ask_multi(self, question: str, run_all: bool = False, company: str = None) -> dict:
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
                "citations": [],
            }

        context, citations = self._get_context_and_citations(question, company=company)

        if not context:
            return {
                "answers": {"General": "No matching documents found for this company/filter."},
                "context_used": "",
                "citations": [],
            }

        if run_all:
            answers = self.router.run_all_agents(context, question)
        else:
            answers = self.router.run_matching_agents(context, question)

        return {
            "answers": answers,
            "context_used": context,
            "citations": citations,
        }

    # ------------------------------------------------------------------
    # NEW: Document Management (Delete & List)
    # ------------------------------------------------------------------

    def get_documents(self):
        return self.vector_store.get_all_documents()

    def delete_document(self, company, source):
        self.vector_store.delete_document(company, source)