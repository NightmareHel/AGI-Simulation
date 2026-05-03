"""
tests/test_integration.py
Full pipeline integration test. Runs all 8 agents against a real Groq API call.
Run: python tests/test_integration.py
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from graph import app
from state import AgentState

TEST_QUERY = "Plan a 3-day trip to Tokyo in June, budget $2000"

if __name__ == "__main__":
    initial_state: AgentState = {
        "original_input": "",
        "user_input": TEST_QUERY,
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

    print("Running full pipeline...\n")
    result = app.invoke(initial_state)

    print("=== DOMAIN ===")
    print(result["domain"])
    print("\n=== SUBTASKS ===")
    for s in result["subtasks"]:
        print(f"  - {s}")
    print("\n=== FLAGGED CLAIMS ===")
    for f in result["flagged_claims"]:
        print(f"  - {f}")
    print("\n=== CONFIDENCE SCORE ===")
    print(result["confidence_score"])
    print("\n=== MEMORY CONTEXT (populated on 2nd run) ===")
    print(result["memory_context"] or "(empty — first run)")
    print("\n=== FINAL OUTPUT ===")
    print(result["final_output"])

    assert result["final_output"], "FAIL: final_output is empty"
    print("\n--- PASS: pipeline completed successfully ---")
