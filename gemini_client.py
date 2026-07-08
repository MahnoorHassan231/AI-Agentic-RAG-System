"""
gemini_client.py
-----------------
Handles all communication with the Gemini LLM. Knows nothing about
PDFs, ChromaDB, or anything else — just talks to Gemini.
"""

import google.generativeai as genai
import config


class GeminiClient:
    def __init__(self):
        if not config.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY is missing. Add GEMINI_API_KEY=xxxx to your .env file."
            )
        genai.configure(api_key=config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(config.GEMINI_MODEL)

    def generate_answer(self, context: str, question: str) -> str:
        """
        Sends the retrieved context + question to Gemini and returns the
        generated answer. This is the core RAG generation step.
        """
        prompt = f"""
You are a helpful assistant. Answer the question ONLY using the context below.
If the answer is not present in the context, say "I don't have enough information in the provided documents."

Context:
{context}

Question:
{question}

Answer:
"""
        response = self.model.generate_content(prompt)
        return response.text.strip()

    def generate_simple(self, prompt: str) -> str:
        """Sends a plain prompt to Gemini with no context (used by the agents)."""
        response = self.model.generate_content(prompt)
        return response.text.strip()