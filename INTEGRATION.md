# AGI-Simulation Integration Plan

**Deadline:** May 4, 2026, 11:59 PM ET (final report due)

**Owner:** Sid (you) — Graph rewiring + Memory Agent implementation

---

## Current State

All agent implementations are on isolated branches. None have been merged into `main` yet.

| Agent | Branch | Owner | Status | File(s) |
|---|---|---|---|---|
| Planner | `planner` | Hamza | Done | `agents/planner.py` |
| Researcher | `researcher` | Bose4life | Done | `agents/researcher.py` |
| Critic | `critic` | Luke | Done | `agents/critic.py` |
| Domain Router | `domain_router` | Luke | Done | `agents/router.py` (not domain_router.py) |
| Fact Checker | `fact_check` | Hamza | Done | `agents/fact_checker.py` |
| Presenter | `Presenter-Agent` | Sid | Done | `agents/presenter.py` |
| Query Rewriter | — | Bose4life | NOT STARTED | To build |
| Memory Agent | — | Sid | TO BUILD | To build |

---

## New Graph Flow

```
User Input
    ↓
[Query Rewriter] ← Bose4life's responsibility
    ↓
[Domain Router] ← Luke's router.py
    ↓
[Memory Agent] ← Sid's responsibility
    ↓
[Planner] ← Hamza's planner.py
    ↓
[Researcher] ← Bose4life's researcher.py
    ↓
[Fact Checker] ← Hamza's fact_checker.py
    ↓
[Critic] ← Luke's critic.py
    ↓
if confidence_score < 0.7 and iteration_count < 3:
    → back to Researcher
else:
    ↓
[Presenter] ← Sid's presenter.py
    ↓
[Memory Agent] ← saves run summary
    ↓
final_output
```

---

## State Schema Changes Required

Current `state.py` (your working version):
```python
class AgentState(TypedDict):
    user_input: str
    subtasks: list[str]
    domain: str
    research_notes: list[str]
    confidence_score: float
    critique: str
    iteration_count: int
    final_output: str
```

Pull from `origin/fact_check` and add these fields:
```python
    flagged_claims: list[str]        # from fact_check branch
    rewritten_query: str             # Query Rewriter output
    memory_context: str              # Memory Agent context injection
```

**Final state.py fields (8 total):**
- `user_input`: str
- `rewritten_query`: str (from Query Rewriter)
- `subtasks`: list[str]
- `domain`: str
- `research_notes`: list[str]
- `confidence_score`: float
- `critique`: str
- `iteration_count`: int
- `flagged_claims`: list[str] (from Fact Checker)
- `memory_context`: str (injected by Memory Agent)
- `final_output`: str

---

## Integration Steps

### Step 1: Update state.py
Cherry-pick the `flagged_claims` field from `origin/fact_check:state.py`, then add `rewritten_query` and `memory_context`.

### Step 2: Implement Memory Agent
File: `agents/memory_agent.py`

**What it does:**
- Runs **before Planner** (startup): reads `memory/runs.jsonl`, injects last 2 runs as context into `state["memory_context"]`
- Runs **after Presenter** (shutdown): appends current run summary to `memory/runs.jsonl`

**Storage:** `memory/runs.jsonl` (gitignored)
Each line is a JSON object:
```json
{
  "timestamp": "2026-04-23T14:30:00Z",
  "user_input": "Plan a trip to Tokyo",
  "domain": "travel",
  "summary": "Found flights $800–$1100, hotels $100–$140/night, activities $30–$80"
}
```

**Implementation notes:**
- Use Groq (llama-3.3-70b-versatile, temp=0.5) to summarize the run (one sentence max)
- For the pre-Planner pass: inject memory_context into the Planner's prompt so it knows prior context
- Graceful fallback: if `memory/runs.jsonl` doesn't exist or is empty, proceed with empty memory_context

### Step 3: Rewire graph.py

Import all agent nodes:
```python
from agents.query_rewriter import query_rewriter_node  # Bose4life will provide
from agents.router import router_node  # Luke's domain_router branch
from agents.memory_agent import memory_agent_pre, memory_agent_post  # Your impl
from agents.planner import planner_node  # Hamza's planner branch
from agents.researcher import researcher_node  # Bose4life's researcher branch
from agents.fact_checker import fact_checker_node  # Hamza's fact_check branch
from agents.critic import critic_node  # Luke's critic branch
from agents.presenter import presenter_node  # Your presenter
```

New edges:
```
Entry → query_rewriter → router → memory_agent_pre → planner → researcher → 
fact_checker → critic → [conditional: loop or proceed] → presenter → memory_agent_post → END
```

Conditional remains: `if confidence_score < 0.7 and iteration_count < 3 → researcher else → presenter`

### Step 4: Integration Testing

Use the existing `tests/test_presenter.py` pattern as a baseline. Create:
- `tests/test_graph_integration.py` — mock state through the full pipeline
- Run with a test query: "Plan a 3-day trip to Tokyo in June, budget $2000"

### Step 5: Merge Strategy

Once all agents are working locally:
1. Create an `integration` branch off `main`
2. Cherry-pick each agent branch into `integration` in order:
   - First: `query_rewriter` (Bose4life's — needs to exist first)
   - Then: `domain_router`
   - Then: `memory_agent` (you'll create)
   - Then: others don't matter, they'll merge fine
3. Resolve any conflicts (mainly in `state.py` if Luke/Hamza touched it)
4. Merge `integration` → `main` when ready to demo

---

## Important Notes for Report Writing

The report (`Seminar Topics final report due May 4`) is the priority. Implementation details are secondary.

**What to highlight in Section 6.2 ("Is Collaboration Enough?"):**
- Memory Agent demonstrates **persistent reasoning** — agents remember prior context
- Fact Checker + Critic show **self-correction** — the system doubts itself and improves
- Query Rewriter + Domain Router show **problem decomposition** — raw input gets refined before processing
- These four additions show **emergent complexity** from multi-agent collaboration

**Simple narrative:** Start with 4 agents (Planner, Researcher, Critic, Presenter). Show that's a loop. Then add 4 more (Memory, Fact-Checker, Query-Rewriter, Domain-Router). Show that emergent behavior increases — the system becomes more robust and self-aware.

---

## Timeline

- **Today (Apr 23):** Initialize Memory Agent + start graph rewiring
- **Apr 24–27:** Finish Memory Agent, complete graph.py, integration test
- **Apr 28–30:** Polish, run full pipeline, document findings
- **May 1–3:** Write final report sections, integrate code findings into narrative
- **May 4, 11:59 PM ET:** Submit final report

---

## File Checklist

After integration, your repo should have:

```
agents/
  ├── __init__.py
  ├── planner.py (from origin/planner)
  ├── researcher.py (from origin/researcher)
  ├── critic.py (from origin/critic)
  ├── router.py (from origin/domain_router)
  ├── fact_checker.py (from origin/fact_check)
  ├── memory_agent.py (NEW — you)
  ├── query_rewriter.py (TBD — Bose4life's branch)
  └── presenter.py (from origin/Presenter-Agent)

prompts/
  ├── planner_prompt.py
  ├── researcher_prompt.py
  ├── critic_prompt.py
  ├── router_prompt.py (from origin/domain_router)
  ├── fact_checker_prompt.py (from origin/fact_check)
  ├── query_rewriter_prompt.py (TBD — Bose4life)
  ├── memory_agent_prompt.py (NEW — you)
  └── presenter_prompt.py

tools/
  └── search.py (needs implementation — Bose4life or someone)

state.py (UPDATED — you)
graph.py (REWRITTEN — you)
main.py (unchanged)

memory/
  └── runs.jsonl (created at runtime, gitignored)

tests/
  ├── test_presenter.py
  └── test_graph_integration.py (NEW — you)
```

---

## Questions to Answer Before Starting

1. **Query Rewriter:** Has Bose4life started? If not, you may need to build a placeholder or coordinate urgently.
2. **tools/search.py:** Is anyone implementing Tavily/Wikipedia search? If not, the Researcher will fail on actual searches.
3. **Memory storage:** Okay with `memory/runs.jsonl` on disk, gitignored? Or prefer a different approach?

