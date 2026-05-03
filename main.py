"""
main.py — Entry Point

Handles CLI input, builds initial AgentState, invokes the compiled LangGraph app,
and prints final output.

CLI modes:
  Single run:  python main.py "Plan a 3-day trip to Tokyo in June, budget $2000"
  Interactive: python main.py  (no args → prompt loop until user types "exit")

Dependencies:
  pip install python-dotenv langgraph langchain langchain-groq tavily-python wikipedia-api
"""

import sys
from dotenv import load_dotenv

from graph import app
from state import AgentState

load_dotenv()


def run(user_input: str) -> str:
    """Invoke the graph for a single user input. Returns final_output."""
    initial_state: AgentState = {
        "original_input": "",
        "user_input": user_input,
        "subtasks": [],
        "domain": "",
        "research_notes": [],
        "confidence_score": 0.0,
        "critique": "",
        "iteration_count": 0,
        "flagged_claims": [],
        "memory_context": "",
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
