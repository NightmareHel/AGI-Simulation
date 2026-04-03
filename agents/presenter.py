from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

from state import AgentState
from prompts.presenter_prompt import PRESENTER_SYSTEM_PROMPT


llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.5)


def presenter_node(state: AgentState) -> AgentState:
    """
    Synthesizes all state into a final user-facing response. Writes to final_output.
    """
    # Build the research context block
    research_context = ""
    for i, (subtask, note) in enumerate(zip(state["subtasks"], state["research_notes"]), 1):
        research_context += f"Subtask {i}: {subtask}\nResearch: {note}\n\n"

    human_message = f"""User request: {state["user_input"]}
Domain: {state["domain"]}

Research gathered:
{research_context.strip()}

Produce the final response for the user."""

    response = llm.invoke([
        SystemMessage(content=PRESENTER_SYSTEM_PROMPT),
        HumanMessage(content=human_message),
    ])

    return {**state, "final_output": response.content}
