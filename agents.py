"""
agents.py
---------
Defines the three AI Agents. Each agent has its own job
(just like a Receptionist, HR, and Manager in an office each do
different things).

This version supports:
1. Single-agent routing (fastest — picks the ONE best-fit agent)
2. Multi-agent routing (runs EVERY agent whose keywords match)
3. "Run all agents" mode (runs all 3 agents regardless of keywords,
   so you can directly compare their answers side-by-side)
"""

import re
from gemini_client import GeminiClient


class AutomationAgent:
    """Job: generate workflows, code snippets, emails, step-by-step plans."""

    name = "Automation"

    def __init__(self, gemini: GeminiClient):
        self.gemini = gemini

    def run(self, context: str, question: str) -> str:
        prompt = f"""
You are an Automation Agent. Based on the context, help create a workflow,
step-by-step plan, or code snippet as requested.

Context:
{context}

Request:
{question}
"""
        return self.gemini.generate_simple(prompt)


class ExtractionAgent:
    """Job: pull specific facts out of documents (dates, amounts, numbers, etc.)."""

    name = "Extraction"

    def __init__(self, gemini: GeminiClient):
        self.gemini = gemini

    def run(self, context: str, question: str) -> str:
        prompt = f"""
You are an Extraction Agent. Extract only the specific facts asked for below,
using the context. Keep the answer short and factual (no extra explanation).

Context:
{context}

Extract:
{question}
"""
        return self.gemini.generate_simple(prompt)


class AnalyticsAgent:
    """Job: analyze data and surface trends / insights / summaries."""

    name = "Analytics"

    def __init__(self, gemini: GeminiClient):
        self.gemini = gemini

    def run(self, context: str, question: str) -> str:
        prompt = f"""
You are an Analytics Agent. Analyze the context and provide insights,
trends, or a summary relevant to the question.

Context:
{context}

Question:
{question}
"""
        return self.gemini.generate_simple(prompt)


class AgentRouter:
    """
    Decides which agent(s) should handle a question, based on keywords.
    Supports single-agent, multi-agent, and "run all" modes.
    """

    def __init__(self, gemini: GeminiClient):
        self.gemini = gemini
        self.automation_agent = AutomationAgent(gemini)
        self.extraction_agent = ExtractionAgent(gemini)
        self.analytics_agent = AnalyticsAgent(gemini)

        self.agent_map = {
            "automation": self.automation_agent,
            "extraction": self.extraction_agent,
            "analytics": self.analytics_agent,
        }

        self.keyword_map = {
            "automation": [
                "workflow", "automate", "automation", "write code", "generate code",
                "python code", "script", "generate a plan", "generate an email",
                "step-by-step plan", "step by step plan",
            ],
            "extraction": [
                "extract", "invoice", "how many", "how much", "what date",
                "total amount", "phone number", "email address",
            ],
            "analytics": [
                "analyze", "analysis", "trend", "profit", "loss", "sales",
                "growth", "insight", "summarize the data", "compare the",
            ],
        }

    # ---------- routing (decide WHICH agents match) ----------

    def route(self, question: str) -> str:
        """Returns the single best-matching agent type using KEYWORD matching (fast, no LLM call)."""
        matches = self.route_multi(question)
        return matches[0] if matches else "general"

    def classify_with_llm(self, question: str) -> str:
        """
        Asks Gemini itself to decide which agent should handle this question.
        More accurate than keyword matching because it understands intent,
        not just exact words (e.g. "show me the trend" -> analytics, even
        though the word "analyze" was never used).
        Falls back to keyword-based routing if the LLM gives an unexpected answer.
        """
        prompt = f"""Classify the following user question into EXACTLY ONE of these categories:

- automation: the user wants a workflow, step-by-step plan, code, or email generated
- extraction: the user wants a specific fact, number, date, or amount pulled from a document
- analytics: the user wants analysis, trends, comparisons, or a summary of data
- general: none of the above — a plain question that should be answered directly from the document

Question: "{question}"

Respond with ONLY one lowercase word: automation, extraction, analytics, or general. No punctuation, no explanation."""

        try:
            raw = self.gemini.generate_simple(prompt).strip().lower()
            for valid_type in ("automation", "extraction", "analytics", "general"):
                if valid_type in raw:
                    return valid_type
        except Exception:
            pass

        # Fallback: keyword-based routing if the LLM call fails or gives junk
        return self.route(question)

    def route_multi(self, question: str) -> list[str]:
        """
        Returns a list of ALL agent types whose keywords match the question.
        Uses WHOLE-WORD matching (via regex word boundaries) so short keywords
        like "code" don't accidentally match inside unrelated words/phrases
        like "dress code".
        """
        q = question.lower()
        matched = []
        for agent_type, keywords in self.keyword_map.items():
            for keyword in keywords:
                pattern = r"\b" + re.escape(keyword) + r"\b"
                if re.search(pattern, q):
                    matched.append(agent_type)
                    break
        return matched

    # ---------- running agents ----------

    def run_agent(self, agent_type: str, context: str, question: str) -> str:
        """Runs exactly one agent by type. 'general' = plain RAG answer via Gemini."""
        agent = self.agent_map.get(agent_type)
        if agent:
            return agent.run(context, question)
        # general -> plain RAG answer (gemini_client's generate_answer)
        return self.gemini.generate_answer(context, question)

    def run_matching_agents(self, context: str, question: str) -> dict[str, str]:
        """
        Runs every agent whose keywords matched the question.
        If nothing matched, falls back to a single general RAG answer.
        Returns {agent_name: answer}.
        """
        matched_types = self.route_multi(question)
        if not matched_types:
            return {"General": self.gemini.generate_answer(context, question)}

        results = {}
        for agent_type in matched_types:
            agent = self.agent_map[agent_type]
            results[agent.name] = agent.run(context, question)
        return results

    def run_all_agents(self, context: str, question: str) -> dict[str, str]:
        """
        Runs ALL three agents regardless of keyword match, so their answers
        can be compared side-by-side. Also includes the plain 'General' RAG answer.
        """
        results = {"General": self.gemini.generate_answer(context, question)}
        for agent_type, agent in self.agent_map.items():
            results[agent.name] = agent.run(context, question)
        return results