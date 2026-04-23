from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

from state import AgentState
from prompts.fact_checker_prompt import FACT_CHECKER_SYSTEM_PROMPT


llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.1)


def fact_checker_node(state: AgentState) -> AgentState:
    """
    Cross-references research_notes for dubious claims. Writes flagged_claims to state.
    """
    notes_block = ""
    for i, (subtask, note) in enumerate(zip(state["subtasks"], state["research_notes"]), 1):
        notes_block += f"Subtask {i}: {subtask}\nResearch: {note}\n\n"

    response = llm.invoke([
        SystemMessage(content=FACT_CHECKER_SYSTEM_PROMPT),
        HumanMessage(content=notes_block.strip()),
    ])

    flagged = []
    text = response.content
    try:
        if "FLAGGED:" in text:
            block = text.split("FLAGGED:", 1)[1].strip()
            if block.lower() != "none":
                for line in block.splitlines():
                    line = line.strip().lstrip("- ").strip()
                    if line:
                        flagged.append(line)
    except Exception:
        pass

    return {**state, "flagged_claims": flagged}
