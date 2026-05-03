from langgraph.graph import StateGraph, END

from state import AgentState
from agents.query_rewriter import query_rewriter_node
from agents.router import router_node
from agents.memory_agent import memory_agent_pre, memory_agent_post
from agents.planner import planner_node
from agents.researcher import researcher_node
from agents.fact_checker import fact_checker_node
from agents.critic import critic_node
from agents.presenter import presenter_node

CONFIDENCE_THRESHOLD = 0.7
MAX_ITERATIONS = 3


def should_continue(state: AgentState) -> str:
    if (
        state["confidence_score"] < CONFIDENCE_THRESHOLD
        and state["iteration_count"] < MAX_ITERATIONS
    ):
        return "researcher"
    return "presenter"


def build_graph() -> StateGraph:
    graph = StateGraph(AgentState)

    graph.add_node("query_rewriter", query_rewriter_node)
    graph.add_node("router", router_node)
    graph.add_node("memory_agent_pre", memory_agent_pre)
    graph.add_node("planner", planner_node)
    graph.add_node("researcher", researcher_node)
    graph.add_node("fact_checker", fact_checker_node)
    graph.add_node("critic", critic_node)
    graph.add_node("presenter", presenter_node)
    graph.add_node("memory_agent_post", memory_agent_post)

    graph.set_entry_point("query_rewriter")

    graph.add_edge("query_rewriter", "router")
    graph.add_edge("router", "memory_agent_pre")
    graph.add_edge("memory_agent_pre", "planner")
    graph.add_edge("planner", "researcher")
    graph.add_edge("researcher", "fact_checker")
    graph.add_edge("fact_checker", "critic")

    graph.add_conditional_edges(
        "critic",
        should_continue,
        {
            "researcher": "researcher",
            "presenter": "presenter",
        },
    )

    graph.add_edge("presenter", "memory_agent_post")
    graph.add_edge("memory_agent_post", END)

    return graph


app = build_graph().compile()
