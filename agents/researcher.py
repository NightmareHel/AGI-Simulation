"""
agents/researcher.py — Researcher Agent

The Researcher is the second node in the graph (and the loop target when the Critic
rejects). It receives the list of subtasks from the Planner (and any critique from
a prior Critic pass) and gathers information to address each subtask.

What this function does:
- Takes AgentState with subtasks (and optionally critique) populated
- For each subtask, calls a search tool or reasons from LLM knowledge
- Writes gathered information back to state as research_notes (list[str])

What to implement:
1. Import the search tool from tools/search.py
2. Load the researcher system prompt from prompts/researcher_prompt.py
3. For each subtask:
   a. Call the search tool with the subtask as a query (if search is enabled)
   b. Pass search results + subtask to the LLM to synthesize a research note
   c. Append the note to research_notes
4. If critique is non-empty (loop case), include it in the LLM prompt so the
   Researcher knows what gaps to address
5. Return updated state with research_notes populated

LLM config:
- Model: gpt-4o-mini
- Temperature: 0.3

Search tool:
- Import run_search() from tools/search.py
- Each call returns a string of search results
- If search is disabled (no API key), skip the tool call and let the LLM reason alone

Notes:
- research_notes should be one entry per subtask (parallel structure with subtasks list)
- If iteration_count > 0, the critique field will be non-empty — use it
- Keep each research note focused and factual — the Critic grades these
"""

from state import AgentState


def researcher_node(state: AgentState) -> AgentState:
    """
    Receives subtasks (and optional critique), returns state with research_notes populated.
    """
    # TODO: initialize LLM
    # TODO: load researcher system prompt
    # TODO: import and call run_search() from tools/search.py for each subtask
    # TODO: synthesize search results into research_notes via LLM
    # TODO: if state["critique"] is non-empty, pass it into the prompt
    # TODO: return updated state

    raise NotImplementedError("Implement researcher_node")
