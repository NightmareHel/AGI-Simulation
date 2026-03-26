"""
agents/presenter.py — Presenter Agent

The Presenter is the final node. It takes everything accumulated in state and
formats it into a clean, readable response for the user.

What this function does:
- Takes AgentState with subtasks, research_notes, and all other fields populated
- Sends the full context to the LLM with instructions to produce a final answer
- Writes the formatted output to state["final_output"]

What to implement:
1. Load the presenter system prompt from prompts/presenter_prompt.py
2. Build a prompt that includes:
   - The original user_input (so the LLM knows what was asked)
   - The subtasks (structure)
   - The research_notes (content)
3. Instruct the LLM to produce a well-formatted, user-facing response
   (e.g. for a trip plan: day-by-day itinerary with budget breakdown)
4. Write the LLM response directly to state["final_output"]
5. Return updated state

LLM config:
- Model: gpt-4o (use the stronger model here — this is what the user sees)
- Temperature: 0.5 (some creativity is fine for presentation)

Notes:
- The Presenter should synthesize, not just concatenate research_notes
- If the domain is "travel", format as an itinerary; if "research", format as a report
- Keep domain-specific formatting logic in the prompt, not in Python code
- final_output is a plain string — main.py will print it directly
"""

from state import AgentState


def presenter_node(state: AgentState) -> AgentState:
    """
    Synthesizes all state into a final user-facing response. Writes to final_output.
    """
    # TODO: initialize LLM (use gpt-4o for best output quality)
    # TODO: load presenter system prompt
    # TODO: build prompt with user_input, subtasks, and research_notes
    # TODO: invoke LLM and write response to state["final_output"]
    # TODO: return updated state

    raise NotImplementedError("Implement presenter_node")
