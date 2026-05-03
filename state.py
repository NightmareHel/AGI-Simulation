from typing import TypedDict


class AgentState(TypedDict):
    original_input: str        # raw user input before rewriting
    user_input: str            # rewritten query (overwritten by query_rewriter_node)
    subtasks: list[str]        # planner output
    domain: str                # router output
    research_notes: list[str]  # researcher output
    confidence_score: float    # critic output
    critique: str              # critic output
    iteration_count: int       # incremented by critic each pass
    flagged_claims: list[str]  # fact_checker output
    memory_context: str        # injected by memory_agent_pre
    final_output: str          # presenter output
