"""
agents/critic.py — Critic Agent

The Critic is the third node in the graph. It receives the subtasks from the Planner
and the research notes from the Researcher, then uses an LLM to evaluate how well
the notes address each subtask.

The LLM responds with a SCORE (0.0–1.0) and a CRITIQUE explaining any gaps.
These are parsed via regex and written back to state. If parsing fails, score
defaults to 0.5 and the raw response is stored as the critique.

iteration_count is incremented here on every pass. graph.py uses the score and
count to decide whether to loop back to the Researcher or proceed to the Presenter.

Model: llama-3.3-70b-versatile via Groq, temperature 0.1 for consistent scoring.
"""

import re

from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

from state import AgentState
from prompts.critic_prompt import CRITIC_SYSTEM_PROMPT


def critic_node(state: AgentState) -> AgentState:
    """
    Evaluates research_notes, returns state with confidence_score, critique,
    and incremented iteration_count.
    """
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.1)

    subtasks_text = "\n".join(
        f"{i+1}. {task}" for i, task in enumerate(state["subtasks"])
    )
    notes_text = "\n".join(
        f"{i+1}. {note}" for i, note in enumerate(state["research_notes"])
    )

    user_message = (
        f"SUBTASKS:\n{subtasks_text}\n\n"
        f"RESEARCH NOTES:\n{notes_text}"
    )

    response = llm.invoke([
        SystemMessage(content=CRITIC_SYSTEM_PROMPT),
        HumanMessage(content=user_message),
    ])
    raw = response.content.strip()

    score = 0.5
    score_match = re.search(r"SCORE:\s*([0-9]*\.?[0-9]+)", raw)
    if score_match:
        try:
            score = float(score_match.group(1))
            score = max(0.0, min(1.0, score))
        except ValueError:
            pass

    critique = raw
    critique_match = re.search(r"CRITIQUE:\s*(.+)", raw, re.DOTALL)
    if critique_match:
        critique = critique_match.group(1).strip()
        if critique.lower() == "none":
            critique = ""

    return {
        **state,
        "confidence_score": score,
        "critique": critique,
        "iteration_count": state["iteration_count"] + 1,
    }
