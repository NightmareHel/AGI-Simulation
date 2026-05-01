"""
state.py — Shared State Schema

This file defines the AgentState TypedDict that flows through every node in the
LangGraph graph. Every agent reads from and writes to this shared object.

What goes here:
- The TypedDict class (AgentState) with all fields the graph needs
- Fields include: user input, planner output (subtasks), researcher output (gathered info),
  critic output (score + critique text), presenter output (final formatted response),
  iteration count (to cap the critic loop), and any domain metadata

Why this file exists:
- LangGraph requires a defined state schema passed between nodes
- Centralizing it here means every agent imports from one place — no drift

How to extend:
- Add a new field to AgentState when a new agent needs to write data
- Keep types tight (str, list[str], int, float) — avoid nested dicts unless necessary
"""

from typing import TypedDict, Optional


class AgentState(TypedDict):
    # Raw input from the user (preserved by query_rewriter before rewriting)
    original_input: str

    # Rewritten input — cleaned and clarified by the query_rewriter, used by all downstream agents
    user_input: str

    # Planner output: list of subtasks broken down from the user request
    subtasks: list[str]

    # Domain identified by the planner (e.g. "travel", "research", "general")
    domain: str

    # Researcher output: raw information gathered per subtask
    research_notes: list[str]

    # Critic output: confidence score between 0.0 and 1.0
    confidence_score: float

    # Critic output: written critique explaining gaps or issues (empty string if passing)
    critique: str

    # Number of times the critic has sent flow back to the researcher
    iteration_count: int

    # Presenter output: the final formatted response shown to the user
    final_output: str
