"""
agents/critic.py — Critic Agent

The Critic is the third node. It evaluates the Researcher's output and decides
whether it is good enough to pass to the Presenter, or whether the Researcher
needs to loop back and try again.

What this function does:
- Takes AgentState with research_notes populated
- Sends the original subtasks + research_notes to the LLM for evaluation
- Parses the LLM response for:
    a. A confidence score (float between 0.0 and 1.0)
    b. A written critique explaining what is missing or weak (can be empty if passing)
- Increments iteration_count by 1
- Writes confidence_score, critique, and updated iteration_count back to state

What to implement:
1. Load the critic system prompt from prompts/critic_prompt.py
2. Build a prompt that includes subtasks and research_notes side by side
3. Instruct the LLM to respond in a structured format, e.g.:
     SCORE: 0.85
     CRITIQUE: The hotel options lack pricing details. Flight info is solid.
4. Parse the response to extract score (float) and critique (str)
5. Increment state["iteration_count"]
6. Return updated state

LLM config:
- Model: gpt-4o-mini
- Temperature: 0.1 (very low — you want consistent scoring, not creative variance)

Parsing tips:
- Use regex or simple string split to extract SCORE and CRITIQUE from the response
- If parsing fails, default score to 0.5 and critique to the raw response

Graph behavior downstream:
- graph.py reads confidence_score and iteration_count to decide the next node
- The Critic itself does not decide routing — it only writes scores to state
"""

from state import AgentState


def critic_node(state: AgentState) -> AgentState:
    """
    Evaluates research_notes, returns state with confidence_score, critique,
    and incremented iteration_count.
    """
    # TODO: initialize LLM
    # TODO: load critic system prompt
    # TODO: build prompt with subtasks and research_notes
    # TODO: invoke LLM and parse SCORE + CRITIQUE from response
    # TODO: handle parse failures gracefully
    # TODO: increment state["iteration_count"]
    # TODO: return updated state

    raise NotImplementedError("Implement critic_node")
