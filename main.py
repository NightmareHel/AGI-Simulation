"""
main.py — Entry Point

This is where the program starts. It handles:
1. Loading environment variables (.env file)
2. Taking user input (CLI loop or single run)
3. Building the initial AgentState
4. Invoking the compiled LangGraph app
5. Printing the final output to the user

What to implement:
- Load .env with python-dotenv (for OPENAI_API_KEY, TAVILY_API_KEY)
- Accept input via sys.argv or an interactive input() loop
- Initialize AgentState with user_input set and all other fields at defaults
- Call app.invoke(initial_state) — this runs the full graph
- Print state["final_output"] when the graph finishes

CLI modes to support:
  Single run:  python main.py "Plan a 3-day trip to Tokyo in June, budget $2000"
  Interactive: python main.py  (no args → prompt loop until user types "exit")

Default initial state values:
  subtasks: []
  domain: ""
  research_notes: []
  confidence_score: 0.0
  critique: ""
  iteration_count: 0
  final_output: ""

Dependencies:
  pip install python-dotenv langgraph langchain langchain-openai
"""

import sys
from dotenv import load_dotenv

from graph import app
from state import AgentState

load_dotenv()


def run(user_input: str) -> str:
    """Invoke the graph for a single user input. Returns final_output."""
    initial_state: AgentState = {
        "user_input": user_input,
        "subtasks": [],
        "domain": "",
        "research_notes": [],
        "confidence_score": 0.0,
        "critique": "",
        "iteration_count": 0,
        "final_output": "",
    }

    result = app.invoke(initial_state)
    return result["final_output"]


def main():
    if len(sys.argv) > 1:
        # Single-run mode: python main.py "your query here"
        query = " ".join(sys.argv[1:])
        print(run(query))
    else:
        # Interactive loop
        print("AGI Simulation — type your request or 'exit' to quit.\n")
        while True:
            try:
                query = input("> ").strip()
            except (KeyboardInterrupt, EOFError):
                break
            if query.lower() in ("exit", "quit", "q"):
                break
            if not query:
                continue
            print("\n" + run(query) + "\n")


if __name__ == "__main__":
    main()
