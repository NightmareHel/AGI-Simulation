"""
tests/test_integration.py
Full pipeline integration test. Runs all 8 agents across multiple query domains.
Each query produces a separate log file in logs/log#.txt.
Run: python tests/test_integration.py
"""

import sys
import os
import re
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from graph import app
from state import AgentState

LOGS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")

TEST_QUERIES = [
    "Plan a 3-day trip to Tokyo in June, budget $2000",                                          # travel
    "What are the symptoms and treatment options for type 2 diabetes?",                          # medical
    "How does CRISPR gene editing work and what are its current applications?",                  # scientific
    "What are my rights if my landlord enters my apartment without notice in Pennsylvania?",     # legal
    "What is the best strategy for paying off student loans while also investing?",              # financial
    "What is the best recipe for a chocolate lava cake?",                                        # unknown/general — food
    "Who would win in a fight between a lion and a tiger?",                                      # unknown/general — ambiguous
]


def get_next_log_number() -> int:
    """Find the next available log number based on existing files in logs/."""
    if not os.path.exists(LOGS_DIR):
        os.makedirs(LOGS_DIR)
    existing = [f for f in os.listdir(LOGS_DIR) if re.match(r"log\d+\.txt", f)]
    if not existing:
        return 1
    numbers = [int(re.search(r"\d+", f).group()) for f in existing]
    return max(numbers) + 1


def run_query(query: str) -> dict:
    initial_state: AgentState = {
        "original_input": "",
        "user_input": query,
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
    return app.invoke(initial_state)


def format_log(query: str, result: dict, run_index: int, total: int, timestamp: str) -> str:
    flagged = "\n".join(f"  - {f}" for f in result["flagged_claims"]) or "  (none)"
    subtasks = "\n".join(f"  {i+1}. {s}" for i, s in enumerate(result["subtasks"]))
    memory = result["memory_context"] or "(empty — first run or no prior context)"

    return f"""AGI-Simulation Pipeline Run
============================
Timestamp : {timestamp}
Query #{run_index} of {total}

ORIGINAL QUERY
--------------
{query}

REWRITTEN QUERY
---------------
{result["user_input"].split("[Prior context")[0].strip()}

DOMAIN
------
{result["domain"]}

MEMORY CONTEXT INJECTED
------------------------
{memory}

SUBTASKS
--------
{subtasks}

FLAGGED CLAIMS
--------------
{flagged}

CONFIDENCE SCORE
----------------
{result["confidence_score"]}

ITERATIONS
----------
{result["iteration_count"]}

FINAL OUTPUT
------------
{result["final_output"]}
"""


def write_log(content: str, log_number: int):
    os.makedirs(LOGS_DIR, exist_ok=True)
    path = os.path.join(LOGS_DIR, f"log{log_number}.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path


if __name__ == "__main__":
    total = len(TEST_QUERIES)
    start_log = get_next_log_number()

    print(f"Running {total} queries — logs will be written to logs/log{start_log}.txt through log{start_log + total - 1}.txt\n")

    for i, query in enumerate(TEST_QUERIES):
        log_number = start_log + i
        print(f"[{i+1}/{total}] Running: \"{query[:60]}...\"" if len(query) > 60 else f"[{i+1}/{total}] Running: \"{query}\"")

        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        result = run_query(query)

        log_content = format_log(query, result, i + 1, total, timestamp)
        path = write_log(log_content, log_number)

        print(f"    Domain: {result['domain']} | Score: {result['confidence_score']} | Iterations: {result['iteration_count']} | Log: logs/log{log_number}.txt\n")

        assert result["final_output"], f"FAIL: final_output empty for query: {query}"

    print(f"--- ALL {total} RUNS PASSED --- logs saved to logs/log{start_log}.txt through log{start_log + total - 1}.txt ---")
