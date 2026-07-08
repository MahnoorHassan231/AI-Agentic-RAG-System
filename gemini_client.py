"""
gemini_client.py
-----------------
Iska sirf ek kaam hai: Gemini LLM se baat karna.
Ye file kisi aur cheez (PDF, ChromaDB) ke baare mein kuch nahi jaanti.
"""

import google.generativeai as genai
import config


class GeminiClient:
    def __init__(self):
        if not config.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY missing hai. .env file mein GEMINI_API_KEY=xxxx daalein."
            )
        genai.configure(api_key=config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(config.GEMINI_MODEL)

    def generate_answer(self, context: str, question: str) -> str:
        """
        Context (retrieved chunks) + Question ko Gemini ko bhejta hai
        aur final answer wapis deta hai. Yahi RAG ka core step hai.
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
        """Bina context ke seedha Gemini se pooch lena (agents ke liye use hota hai)."""
        response = self.model.generate_content(prompt)
        return response.text.strip()
