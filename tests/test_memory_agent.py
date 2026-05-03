"""
Standalone test for the memory agent.
Bypasses the full graph — tests memory_agent_pre and memory_agent_post in isolation.
Run: python tests/test_memory_agent.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from agents.memory_agent import memory_agent_pre, memory_agent_post

# --- Mock state: simulates what would enter memory_agent_pre ---
mock_state_pre = {
    "original_input": "What are the health benefits of intermittent fasting?",
    "user_input": "What are the documented health benefits of intermittent fasting based on clinical research?",
    "subtasks": [],
    "domain": "medical",
    "research_notes": [],
    "confidence_score": 0.0,
    "critique": "",
    "iteration_count": 0,
    "flagged_claims": [],
    "memory_context": "",
    "final_output": "",
}

# --- Mock state: simulates what would enter memory_agent_post ---
mock_state_post = {
    "original_input": "What are the health benefits of intermittent fasting?",
    "user_input": "What are the documented health benefits of intermittent fasting based on clinical research?",
    "subtasks": [
        "Find clinical studies on intermittent fasting and metabolic health",
        "Identify documented effects on weight loss and insulin sensitivity",
        "Research cardiovascular and cognitive benefits of intermittent fasting",
    ],
    "domain": "medical",
    "research_notes": [
        "Multiple clinical studies show intermittent fasting improves metabolic markers including reduced fasting glucose and insulin levels.",
        "Studies report 3–8% body weight reduction over 8–24 weeks; insulin sensitivity improves significantly in type 2 diabetic patients.",
        "Research links intermittent fasting to lower LDL cholesterol, reduced inflammation markers, and improved cognitive function in animal models.",
    ],
    "confidence_score": 0.91,
    "critique": "",
    "iteration_count": 1,
    "flagged_claims": ["animal model results may not directly translate to humans"],
    "memory_context": "",
    "final_output": (
        "Intermittent fasting has strong clinical support for metabolic and weight-related benefits. "
        "Studies consistently show reduced fasting glucose, improved insulin sensitivity, and 3–8% body "
        "weight reduction over 8–24 weeks. Cardiovascular benefits include lower LDL cholesterol and "
        "reduced inflammation. Cognitive benefits are promising but currently based primarily on animal "
        "models. As always, consult a physician before making dietary changes."
    ),
}


if __name__ == "__main__":
    print("=" * 60)
    print("TEST 1: memory_agent_pre (first run — memory file may be empty)")
    print("=" * 60)
    result_pre = memory_agent_pre(mock_state_pre)
    print(f"memory_context: '{result_pre['memory_context'] or '(empty — no prior runs)'}'")
    print(f"\nuser_input after injection:\n{result_pre['user_input']}")

    print("\n" + "=" * 60)
    print("TEST 2: memory_agent_post (saves this run to memory)")
    print("=" * 60)
    result_post = memory_agent_post(mock_state_post)
    print("Run saved to memory/runs.jsonl")

    print("\n" + "=" * 60)
    print("TEST 3: memory_agent_pre again (should now see saved run)")
    print("=" * 60)
    result_pre2 = memory_agent_pre(mock_state_pre)
    print(f"memory_context:\n{result_pre2['memory_context'] or '(still empty — something went wrong)'}")
    print(f"\nuser_input after injection:\n{result_pre2['user_input']}")

    assert result_pre2["memory_context"], "FAIL: memory_context should be populated on second pre-run"
    print("\n--- PASS: memory agent pre/post cycle working correctly ---")
