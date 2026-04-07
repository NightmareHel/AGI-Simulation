"""
tests/test_researcher.py — Researcher Agent Tests

Runs the researcher_node in isolation using fake planner/critic inputs.
No real graph, no real planner, no real critic -- just the researcher.

Test cases:
1. Basic run       -- fresh subtasks, no critique (first pass)
2. Critique loop   -- subtasks + critique from a prior critic rejection
3. Multi-subtask   -- several subtasks to verify parallel note structure
4. No search       -- forces Wikipedia fallback (unset TAVILY_API_KEY)

Run with:
    python -m pytest tests/test_researcher.py -v
or just:
    python tests/test_researcher.py
"""

import sys
import os

# Allow imports from project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dotenv import load_dotenv
load_dotenv()

from agents.researcher import researcher_node
from state import AgentState


# ---------------------------------------------------------------------------
# Fake state builders -- simulate what the Planner / Critic would produce
# ---------------------------------------------------------------------------

def make_state(
    user_input: str = "Tell me about AI trends in 2025",
    subtasks: list[str] = None,
    domain: str = "research",
    critique: str = "",
    iteration_count: int = 0,
) -> AgentState:
    return AgentState(
        user_input=user_input,
        subtasks=subtasks or ["What are the major AI trends in 2025?"],
        domain=domain,
        research_notes=[],
        confidence_score=0.0,
        critique=critique,
        iteration_count=iteration_count,
        final_output="",
    )


# ---------------------------------------------------------------------------
# Test 1: Basic first-pass research (no critique)
# ---------------------------------------------------------------------------

def test_basic_research():
    print("\n--- Test 1: Basic first-pass research ---")

    state = make_state(
        user_input="What are the best practices for REST API design?",
        subtasks=[
            "What are common REST API design principles?",
            "What HTTP status codes should REST APIs use?",
        ],
        domain="research",
    )

    result = researcher_node(state)

    assert "research_notes" in result
    assert len(result["research_notes"]) == 2, "Should have one note per subtask"

    for i, note in enumerate(result["research_notes"]):
        assert isinstance(note, str), f"Note {i} should be a string"
        assert len(note) > 50, f"Note {i} seems too short: {note!r}"
        print(f"  Subtask {i+1} note ({len(note)} chars): {note[:120]}...")

    print("  PASSED")


# ---------------------------------------------------------------------------
# Test 2: Critique loop (simulates Critic rejecting and sending back)
# ---------------------------------------------------------------------------

def test_research_with_critique():
    print("\n--- Test 2: Research with prior critique ---")

    state = make_state(
        user_input="Explain the causes of the 2008 financial crisis",
        subtasks=[
            "What were the main causes of the 2008 financial crisis?",
        ],
        domain="research",
        critique=(
            "The research note lacks specific detail about the role of mortgage-backed "
            "securities and credit default swaps. Also missing: which banks failed and when."
        ),
        iteration_count=1,
    )

    result = researcher_node(state)

    assert len(result["research_notes"]) == 1
    note = result["research_notes"][0]

    print(f"  Note ({len(note)} chars): {note[:200]}...")

    # Rough check that critique influenced the output
    keywords = ["mortgage", "securities", "bank", "credit", "swap", "2008"]
    hits = [kw for kw in keywords if kw.lower() in note.lower()]
    print(f"  Critique-relevant keywords found: {hits}")
    assert len(hits) >= 2, f"Expected critique to steer output, only found: {hits}"

    print("  PASSED")


# ---------------------------------------------------------------------------
# Test 3: Multi-subtask -- verifies 1:1 note-to-subtask structure
# ---------------------------------------------------------------------------

def test_multi_subtask():
    print("\n--- Test 3: Multi-subtask structure ---")

    subtasks = [
        "What is machine learning?",
        "What is the difference between supervised and unsupervised learning?",
        "What are common machine learning frameworks?",
        "What industries use machine learning the most?",
    ]

    state = make_state(
        user_input="Give me an overview of machine learning",
        subtasks=subtasks,
        domain="research",
    )

    result = researcher_node(state)

    assert len(result["research_notes"]) == len(subtasks), (
        f"Expected {len(subtasks)} notes, got {len(result['research_notes'])}"
    )

    for i, note in enumerate(result["research_notes"]):
        assert len(note) > 30, f"Note {i} too short"
        print(f"  [{i+1}] {note[:100]}...")

    print("  PASSED")


# ---------------------------------------------------------------------------
# Test 4: State passthrough -- non-researcher fields stay untouched
# ---------------------------------------------------------------------------

def test_state_passthrough():
    print("\n--- Test 4: State passthrough integrity ---")

    state = make_state(
        user_input="Original input",
        subtasks=["What is quantum computing?"],
        domain="science",
        critique="",
        iteration_count=2,
    )

    result = researcher_node(state)

    assert result["user_input"] == "Original input"
    assert result["domain"] == "science"
    assert result["iteration_count"] == 2
    assert result["final_output"] == ""
    assert result["confidence_score"] == 0.0

    print("  All non-researcher fields preserved correctly")
    print("  PASSED")


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    tests = [
        test_basic_research,
        test_research_with_critique,
        test_multi_subtask,
        test_state_passthrough,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"  FAILED: {e}")
            failed += 1

    print(f"\n{passed} passed, {failed} failed")
