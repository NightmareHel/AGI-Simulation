"""
test_router.py — Domain Router Isolation Test

Runs router_node against two hardcoded states simulating what the Query
Rewriter would have passed in:

  TEST 1: Clear domain — a clean travel query, should classify as "travel"
  TEST 2: Ambiguous query — vague input that should fall back to "general"

Run:
    .venv/bin/python test_router.py
"""

from dotenv import load_dotenv
load_dotenv()

from agents.router import router_node

travel_state = {
    "user_input": "Plan a 3-day trip to Tokyo in June with a budget of $2000, including flights, hotels, and activities.",
    "subtasks": [],
    "domain": "",
    "research_notes": [],
    "confidence_score": 0.0,
    "critique": "",
    "iteration_count": 0,
    "final_output": "",
}

ambiguous_state = {
    "user_input": "What should I do?",
    "subtasks": [],
    "domain": "",
    "research_notes": [],
    "confidence_score": 0.0,
    "critique": "",
    "iteration_count": 0,
    "final_output": "",
}


def run_test(label: str, state: dict, expected_domain: str):
    print(f"=== {label} ===")
    result = router_node(state)
    print(f"domain : {result['domain']!r}")

    assert isinstance(result["domain"], str), "domain must be a string"
    assert result["domain"] in {"medical", "scientific", "legal", "financial", "travel", "general"}, \
        f"domain must be a valid domain, got {result['domain']!r}"
    assert result["domain"] == expected_domain, \
        f"Expected {expected_domain!r}, got {result['domain']!r}"

    print("Assertions passed.\n")


run_test("TEST 1: CLEAR TRAVEL QUERY", travel_state, expected_domain="travel")
run_test("TEST 2: AMBIGUOUS QUERY", ambiguous_state, expected_domain="general")
