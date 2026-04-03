"""
Standalone test for the presenter agent.
Bypasses the full graph — feeds mock state directly into presenter_node.
Run: python tests/test_presenter.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from agents.presenter import presenter_node

# --- Mock state: simulates what the graph would have built up ---
mock_state = {
    "user_input": "Plan a 3-day trip to Tokyo in June, budget $2000",
    "domain": "travel",
    "subtasks": [
        "Find round-trip flights from Philadelphia to Tokyo in June under $1200",
        "Find hotels in Tokyo for 3 nights under $150/night",
        "Find top activities and day trips in Tokyo",
        "Estimate daily food costs in Tokyo",
    ],
    "research_notes": [
        "Round-trip flights from PHL to Tokyo (NRT) in June typically range from $800–$1100 on airlines like ANA and United. Booking 6–8 weeks in advance gets the best rates. Flight time is approximately 14–15 hours nonstop.",
        "Mid-range hotels in Tokyo such as Shinjuku Granbell Hotel or Sotetsu Fresa Inn Akihabara run $100–$140/night. Staying in Shinjuku or Akihabara gives good transit access. Capsule hotels are available from $40/night for budget stretching.",
        "Top activities include Senso-ji Temple in Asakusa (free), Shibuya Crossing and surrounding area (free), teamLab Planets digital art museum ($30), day trip to Nikko or Hakone (~$50–$80 round trip), and Tsukiji Outer Market for food tours.",
        "Budget meals at ramen shops and convenience stores run $8–$12/meal. Mid-range restaurant dinners average $20–$30. A daily food budget of $60–$80 covers three meals comfortably with room for a splurge.",
    ],
    "confidence_score": 0.88,
    "critique": "",
    "iteration_count": 1,
    "final_output": "",
}

if __name__ == "__main__":
    print("Running presenter agent test...\n")
    print("=" * 60)
    result = presenter_node(mock_state)
    print(result["final_output"])
    print("=" * 60)
