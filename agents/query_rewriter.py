"""
agents/query_rewriter.py — Query Rewriter Agent

First node in the graph. Intercepts raw user input before the Planner sees it
and reformulates vague, messy, or ambiguous queries into clean, precise questions.

What this function does:
- Reads user_input from state
- Rewrites it into a clear, specific question using an LLM
- Stores the original raw input in original_input (for reference/debugging)
- Overwrites user_input with the rewritten version so all downstream agents benefit

LLM config:
- Model: llama-3.3-70b-versatile (via Groq)
- Temperature: 0.2 (low — we want deterministic reformulation, not creativity)
"""

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.schema import SystemMessage, HumanMessage

from state import AgentState
from prompts.query_rewriter_prompt import QUERY_REWRITER_SYSTEM_PROMPT

load_dotenv()


def query_rewriter_node(state: AgentState) -> AgentState:
    """
    Rewrites the raw user_input into a clean, precise query before the Planner runs.
    """
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.2,
        groq_api_key=os.getenv("GROQ_API_KEY"),
    )

    raw_input = state.get("user_input", "").strip()

    messages = [
        SystemMessage(content=QUERY_REWRITER_SYSTEM_PROMPT),
        HumanMessage(content=raw_input),
    ]

    response = llm.invoke(messages)
    rewritten = response.content.strip()

    return {
        **state,
        "original_input": raw_input,
        "user_input": rewritten,
    }
