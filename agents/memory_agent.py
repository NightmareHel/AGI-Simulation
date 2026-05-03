import json
import os
from datetime import datetime

from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

from state import AgentState
from prompts.memory_agent_prompt import MEMORY_SUMMARY_PROMPT

MEMORY_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "memory", "runs.jsonl")
MAX_PRIOR_RUNS = 3


def _ensure_memory_dir():
    os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)


def _read_last_runs(n: int) -> list[dict]:
    if not os.path.exists(MEMORY_FILE):
        return []
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]
    runs = []
    for line in lines[-n:]:
        try:
            runs.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    return runs


def memory_agent_pre(state: AgentState) -> AgentState:
    """
    Reads the last 3 runs from memory and injects context into user_input before the Planner.
    No LLM call — pure file read.
    """
    _ensure_memory_dir()
    runs = _read_last_runs(MAX_PRIOR_RUNS)

    if not runs:
        return {**state, "memory_context": ""}

    lines = []
    for r in runs:
        summary = r.get("summary", "")
        domain = r.get("domain", "")
        ts = r.get("timestamp", "")
        if summary:
            lines.append(f"- [{ts[:10]} | {domain}] {summary}")

    memory_context = "\n".join(lines)
    injected_input = state["user_input"] + f"\n\n[Prior context from memory:\n{memory_context}]"

    return {
        **state,
        "memory_context": memory_context,
        "user_input": injected_input,
    }


def memory_agent_post(state: AgentState) -> AgentState:
    """
    Saves a one-sentence summary of the current run to memory/runs.jsonl.
    Uses Groq to generate the summary. Returns state unchanged.
    """
    _ensure_memory_dir()

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.3,
        groq_api_key=os.getenv("GROQ_API_KEY"),
    )

    human_content = (
        f"User asked: {state.get('original_input') or state.get('user_input', '')}\n\n"
        f"Final answer: {state.get('final_output', '')}"
    )

    response = llm.invoke([
        SystemMessage(content=MEMORY_SUMMARY_PROMPT),
        HumanMessage(content=human_content),
    ])
    summary = response.content.strip()

    record = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "user_input": state.get("original_input") or state.get("user_input", ""),
        "domain": state.get("domain", ""),
        "summary": summary,
    }

    with open(MEMORY_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")

    return state
