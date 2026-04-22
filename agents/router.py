"""
agents/router.py — Domain Router Agent

The Domain Router is the second node in the graph, sitting after the Query
Rewriter and before the Planner. It receives the rewritten user query and
classifies it into a domain so downstream agents know how to handle it.

It sends the query to the LLM with a strict classification prompt and parses
a single domain from the response. If parsing fails or the domain is not in
the supported list, it defaults to "general".

Writes domain to state. That's it — no scoring, no looping, one clean output.

Model: llama-3.3-70b-versatile via Groq, temperature 0.0 for deterministic classification.
"""

import re

from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

from state import AgentState
from prompts.router_prompt import ROUTER_SYSTEM_PROMPT

VALID_DOMAINS = {"medical", "scientific", "legal", "financial", "travel", "general"}


def router_node(state: AgentState) -> AgentState:
    """
    Classifies the user query into a domain and writes it to state.
    """
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.0)

    response = llm.invoke([
        SystemMessage(content=ROUTER_SYSTEM_PROMPT),
        HumanMessage(content=state["user_input"]),
    ])
    raw = response.content.strip()

    domain = "general"
    match = re.search(r"DOMAIN:\s*(\w+)", raw, re.IGNORECASE)
    if match:
        parsed = match.group(1).lower()
        if parsed in VALID_DOMAINS:
            domain = parsed

    return {
        **state,
        "domain": domain,
    }
