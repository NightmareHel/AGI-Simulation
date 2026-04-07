"""
test_critic.py — Critic Agent Isolation Test

Runs critic_node against two hardcoded states:
  - TEST 1: Good research — specific, detailed, all subtasks addressed
  - TEST 2: Bad research — vague, missing numbers, one subtask not addressed

Both use the same user query and subtasks so the quality difference is clear.

Run:
    .venv/bin/python test_critic.py
"""

from dotenv import load_dotenv
load_dotenv()

from agents.critic import critic_node

SUBTASKS = [
    "Find round-trip flights from New York to Tokyo in June under $1200",
    "Find hotels in Tokyo for 3 nights under $150/night",
    "Find top activities and day trips in Tokyo",
    "Estimate daily food costs in Tokyo",
]

good_state = {
    "user_input": "Plan a 3-day trip to Tokyo in June, budget $2000",
    "subtasks": SUBTASKS,
    "domain": "travel",
    "research_notes": [
        "Round-trip flights from JFK to Tokyo (NRT) in June typically range from $800–$1100 on carriers like JAL and ANA. Booking 6–8 weeks in advance is recommended.",
        "Budget hotels in Shinjuku and Asakusa average $90–$130/night. Options include Dormy Inn Asakusa ($95/night) and Keio Presso Inn Shinjuku ($110/night).",
        "Top activities include Senso-ji Temple (free), teamLab Borderless ($32), day trip to Nikko ($40 round-trip by train), and Shibuya Crossing.",
        "Daily food costs in Tokyo average $30–$50. Convenience store meals cost $3–$6; ramen shops average $8–$12; mid-range restaurants $15–$25.",
    ],
    "confidence_score": 0.0,
    "critique": "",
    "iteration_count": 0,
    "final_output": "",
}

bad_state = {
    "user_input": "Plan a 3-day trip to Tokyo in June, budget $2000",
    "subtasks": SUBTASKS,
    "domain": "travel",
    "research_notes": [
        "There are flights available from the US to Tokyo in June. Prices vary depending on the airline.",
        "Hotels in Tokyo can be found in many neighborhoods. Some are cheap and some are expensive.",
        "Tokyo has many things to do including temples and food.",
        "", 
    ],
    "confidence_score": 0.0,
    "critique": "",
    "iteration_count": 0,
    "final_output": "",
}


def run_test(label: str, state: dict, expected_pass: bool):
    print(f"=== {label} ===")
    result = critic_node(state)
    print(f"confidence_score : {result['confidence_score']}")
    print(f"iteration_count  : {result['iteration_count']}")
    print(f"critique         : {result['critique']!r}")

    assert isinstance(result["confidence_score"], float), "confidence_score must be a float"
    assert 0.0 <= result["confidence_score"] <= 1.0, "confidence_score must be between 0 and 1"
    assert result["iteration_count"] == 1, "iteration_count must be incremented to 1"
    assert isinstance(result["critique"], str), "critique must be a string"

    if expected_pass:
        assert result["confidence_score"] >= 0.7, f"Expected good research to score >= 0.7, got {result['confidence_score']}"
    else:
        assert result["confidence_score"] < 0.7, f"Expected bad research to score < 0.7, got {result['confidence_score']}"

    print("Assertions passed.\n")


run_test("TEST 1: GOOD RESEARCH", good_state, expected_pass=True)
run_test("TEST 2: BAD RESEARCH", bad_state, expected_pass=False)
