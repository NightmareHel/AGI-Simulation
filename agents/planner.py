"""
agents/planner.py — Planner Agent

The Planner is the first node in the graph. It receives raw user input and is
responsible for understanding what the user wants and breaking it into concrete
subtasks that the Researcher can act on.

What this function does:
- Takes the AgentState (with user_input populated)
- Sends user_input to the LLM with the planner system prompt
- Parses the LLM response into a list of subtasks
- Identifies the domain (e.g. "travel", "research", "general")
- Writes subtasks and domain back into state

What to implement:
1. Import the LLM client (ChatOpenAI from langchain_openai)
2. Load the planner system prompt from prompts/planner_prompt.py
3. Build a prompt that includes user_input
4. Call the LLM and parse the response — subtasks can be a numbered list in the response,
   split by newline into a Python list
5. Return the updated state dict with subtasks and domain set

LLM config:
- Model: gpt-4o-mini is cost-efficient for planning tasks
- Temperature: 0.3 (lower = more structured output)

Notes:
- Keep parsing simple — if the LLM returns "1. X\n2. Y\n3. Z", split on newlines and strip
- If parsing fails, fall back to treating the whole response as one subtask
- Do not call external tools here — this is reasoning only
"""

from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

from state import AgentState
from prompts.planner_prompt import PLANNER_SYSTEM_PROMPT


llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.3)


def planner_node(state: AgentState) -> AgentState:
    """
    Receives user_input, returns state with subtasks and domain populated.
    """
    response = llm.invoke([
        SystemMessage(content=PLANNER_SYSTEM_PROMPT),
        HumanMessage(content=state["user_input"]),
    ])

    text = response.content
    domain = "general"
    subtasks = []

    try:
        for line in text.splitlines():
            line = line.strip()
            if line.startswith("DOMAIN:"):
                domain = line.replace("DOMAIN:", "").strip().lower()
            elif line and line[0].isdigit() and "." in line:
                subtasks.append(line.split(".", 1)[1].strip())
    except Exception:
        pass

    if not subtasks:
        subtasks = [text.strip()]

    return {**state, "subtasks": subtasks, "domain": domain}
