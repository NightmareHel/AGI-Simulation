"""
graph.py — LangGraph Graph Definition

This file builds, wires, and compiles the LangGraph graph. It is the coordination
layer — it does not contain any LLM logic itself. It only defines:

  1. Which nodes exist (each agent function)
  2. The edges between them (linear and conditional)
  3. The entry point and any terminal nodes
  4. The compiled graph object, which main.py imports and invokes

What goes here:
- Import each agent function from agents/
- Register each as a node via graph.add_node()
- Define normal edges (planner → researcher, critic pass → presenter)
- Define the conditional edge after the critic node:
    if confidence_score < CONFIDENCE_THRESHOLD and iteration_count < MAX_ITERATIONS
        → back to researcher
    else
        → presenter
- Compile the graph and export it as `app`

Constants to tune:
- CONFIDENCE_THRESHOLD: float — minimum score for the critic to pass (suggested: 0.7)
- MAX_ITERATIONS: int — max times the critic can send work back (suggested: 3)

How to extend:
- Add a new agent by importing it, calling graph.add_node(), and wiring edges
- Swap in a checkpointer (e.g. MemorySaver) here if you want conversation memory across runs
"""

from langgraph.graph import StateGraph, END

from state import AgentState
from agents.planner import planner_node
from agents.researcher import researcher_node
from agents.critic import critic_node
from agents.presenter import presenter_node

CONFIDENCE_THRESHOLD = 0.7
MAX_ITERATIONS = 3


def should_continue(state: AgentState) -> str:
    """
    Conditional edge function after the critic node.
    Returns "researcher" to loop back, or "presenter" to proceed.
    """
    if (
        state["confidence_score"] < CONFIDENCE_THRESHOLD
        and state["iteration_count"] < MAX_ITERATIONS
    ):
        return "researcher"
    return "presenter"


def build_graph() -> StateGraph:
    graph = StateGraph(AgentState)

    # Register nodes
    graph.add_node("planner", planner_node)
    graph.add_node("researcher", researcher_node)
    graph.add_node("critic", critic_node)
    graph.add_node("presenter", presenter_node)

    # Set entry point
    graph.set_entry_point("planner")

    # Linear edges
    graph.add_edge("planner", "researcher")
    graph.add_edge("researcher", "critic")

    # Conditional edge after critic
    graph.add_conditional_edges(
        "critic",
        should_continue,
        {
            "researcher": "researcher",
            "presenter": "presenter",
        },
    )

    # Terminal edge
    graph.add_edge("presenter", END)

    return graph


# Compiled graph — import this in main.py
app = build_graph().compile()
