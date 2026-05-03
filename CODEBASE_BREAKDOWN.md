# AGI-Simulation Codebase Breakdown

**As of May 3, 2026**

All 7 agents are implemented across 6 branches. Below is a detailed breakdown of what each branch contains and what changes it introduces.

---

## Branch: `origin/planner` (Hamza)

**Last commit:** `cc1943a` — "added planner.py code" (12 days ago)

**Files modified:**
- `agents/planner.py` ✨ NEW
- `prompts/planner_prompt.py` ✨ NEW (already existed in scaffold, refined)

**What it does:**

The Planner is the first reasoning node. It receives the rewritten query (from Query Rewriter) and breaks it into 3–5 concrete subtasks.

**Implementation details:**
```python
def planner_node(state: AgentState) -> AgentState:
    # Uses Groq llama-3.3-70b-versatile, temperature=0.3
    # Input: state["user_input"] (already rewritten)
    # Output: state["subtasks"], state["domain"]
    
    # Parsing:
    # - Expects LLM response in format:
    #   DOMAIN: <domain>
    #   SUBTASKS:
    #   1. <subtask>
    #   2. <subtask>
    # - Splits on "DOMAIN:" and numbered list markers
    # - Falls back to treating whole response as one subtask if parsing fails
```

**Prompt philosophy:**
- Explicit output format (DOMAIN: / SUBTASKS:)
- Strictly 3–5 subtasks max
- Does not answer the question — only plans
- Domains supported: travel, research, general (hard-coded, not restrictive)

**State changes:** None (uses existing fields)

---

## Branch: `origin/researcher` (Bose4life)

**Last commit:** `eea25cb` — "Add query rewriter agent as pipeline entry point" (9 days ago)

**Files modified:**
- `agents/query_rewriter.py` ✨ NEW
- `agents/researcher.py` ✨ NEW (fully implemented, not stub)
- `prompts/query_rewriter_prompt.py` ✨ NEW
- `prompts/researcher_prompt.py` ✨ NEW (already existed, refined)
- `state.py` 🔄 MODIFIED
- `graph.py` 🔄 MODIFIED

**What it does:**

This branch adds two agents:

### 1. Query Rewriter (Entry point)
```python
def query_rewriter_node(state: AgentState) -> AgentState:
    # Uses Groq llama-3.3-70b-versatile, temperature=0.2 (very low)
    # Input: state["user_input"] (raw messy input)
    # Output: state["user_input"] (rewritten), state["original_input"] (backup)
    
    # Purpose: Clean up vague, messy, or ambiguous user queries
    # Examples:
    #   "uhh whats like the best way to learn coding or whatever idk"
    #   → "What is the most effective approach to learning programming as a beginner?"
    #   "tesla stock thing and also like why did it drop"
    #   → "Why did Tesla's stock price drop recently and what factors contributed to it?"
```

**Query Rewriter prompt philosophy:**
- Remove filler, typos, conversational noise
- Resolve ambiguity by inferring intent
- Preserve original scope
- Output only the rewritten query (no labels, no explanation)

### 2. Researcher (Loop target from Critic)
```python
def researcher_node(state: AgentState) -> AgentState:
    # Uses Groq llama-3.3-70b-versatile, temperature=0.3
    # Input: state["subtasks"], state["critique"] (if looping)
    # Output: state["research_notes"]
    
    # For each subtask:
    # 1. Call run_search(subtask) to get search results (from tools/search.py)
    # 2. Pass subtask + search_results + critique (if any) to LLM
    # 3. LLM synthesizes a factual research note
    # 4. Append to research_notes list
    
    # If iteration_count > 0 and critique is non-empty:
    #   Include critique in the prompt so Researcher knows what gaps to fix
```

**Researcher prompt philosophy:**
- Concise, factual, one paragraph per subtask
- Use search results if provided; synthesize, don't copy
- If critique provided, explicitly address every gap
- Include numbers, names, details
- No opinions or unsolicited recommendations

**State schema changes:**
```python
class AgentState(TypedDict):
    original_input: str         # ← NEW (backup of raw user input)
    user_input: str             # ← UPDATED (now rewritten by query_rewriter)
    subtasks: list[str]         # ← existing
    domain: str                 # ← existing
    research_notes: list[str]   # ← existing
    confidence_score: float     # ← existing
    critique: str               # ← existing
    iteration_count: int        # ← existing
    final_output: str           # ← existing
```

**Graph changes:**
Entry point now starts at `query_rewriter` instead of `planner`.
```
query_rewriter → planner → researcher → critic → [conditional] → presenter
```

---

## Branch: `origin/critic` (Luke)

**Last commit:** `b54496e` — "Implemented the critic agent..." (3 weeks ago)

**Files modified:**
- `agents/critic.py` ✨ NEW (fully implemented, not stub)
- `prompts/critic_prompt.py` ✨ NEW (already existed, refined)

**What it does:**

The Critic evaluates the Researcher's output and decides if it's good enough to pass to Presenter or if the Researcher should loop and try again.

```python
def critic_node(state: AgentState) -> AgentState:
    # Uses Groq llama-3.3-70b-versatile, temperature=0.1 (very low — consistent scoring)
    # Input: state["subtasks"], state["research_notes"]
    # Output: state["confidence_score"], state["critique"], state["iteration_count"] incremented
    
    # 1. Build prompt with subtasks + research_notes side by side
    # 2. LLM responds in format:
    #    SCORE: 0.85
    #    CRITIQUE: The hotel options lack pricing details. Flight info is solid.
    # 3. Parse SCORE and CRITIQUE using regex
    # 4. Clamp score to [0.0, 1.0]
    # 5. If parsing fails, default score=0.5, critique=raw response
    # 6. Increment iteration_count
    # 7. Return updated state
    
    # graph.py uses confidence_score < 0.7 and iteration_count < 3 to decide
    # whether to loop back to Researcher or proceed to Presenter
```

**Critic prompt philosophy:**
- Scoring scale:
  - 0.9–1.0: Thoroughly addressed, specific and detailed
  - 0.7–0.89: Mostly good, minor gaps
  - 0.5–0.69: Significant gaps present
  - Below 0.5: Major issues
- Only identify what's missing, not what's good
- Critique optional if score >= 0.9 ("None" is acceptable)

**State changes:** None (uses existing fields, increments iteration_count)

---

## Branch: `origin/domain_router` (Luke)

**Last commit:** `331966d` — "Implemented the domain router agent..." (9 days ago)

**Files modified:**
- `agents/router.py` ✨ NEW (fully implemented, not stub)
  - **NOTE: File is `router.py`, not `domain_router.py`**
  - Function is `router_node()`
- `prompts/router_prompt.py` ✨ NEW

**What it does:**

The Domain Router runs after Query Rewriter and before Planner. It classifies the query into a domain so downstream agents know how to handle depth and tone.

```python
def router_node(state: AgentState) -> AgentState:
    # Uses Groq llama-3.3-70b-versatile, temperature=0.0 (deterministic)
    # Input: state["user_input"] (rewritten)
    # Output: state["domain"] (overrides planner's domain)
    
    # Supported domains: medical, scientific, legal, financial, travel, general
    # LLM responds in format:
    #    DOMAIN: travel
    # 
    # If parsing fails or domain not in VALID_DOMAINS, defaults to "general"
    # Very simple — no scoring, no looping, one clean output
```

**Router prompt philosophy:**
- Strict classification from fixed list
- Guides downstream agents on handling depth and tone
- If spanning multiple domains, pick the most dominant one
- Output only: "DOMAIN: <domain>"

**State changes:** None (overwrites existing domain field)

---

## Branch: `origin/fact_check` (Hamza)

**Last commit:** `ffd9f10` — "added fact checker agent" (9 days ago)

**Files modified:**
- `agents/fact_checker.py` ✨ NEW (fully implemented, not stub)
- `prompts/fact_checker_prompt.py` ✨ NEW
- `state.py` 🔄 MODIFIED

**What it does:**

The Fact Checker runs after Researcher and before Critic. It cross-references research notes for dubious, vague, unverifiable, or contradictory claims.

```python
def fact_checker_node(state: AgentState) -> AgentState:
    # Uses Groq llama-3.3-70b-versatile, temperature=0.1
    # Input: state["subtasks"], state["research_notes"]
    # Output: state["flagged_claims"]
    
    # 1. Build block with subtask + research note pairs
    # 2. LLM responds in format:
    #    FLAGGED:
    #    - <suspicious claim>
    #    - <suspicious claim>
    #    or
    #    FLAGGED: none
    # 3. Parse the list of flagged claims
    # 4. If parsing fails, returns empty list
    # 5. Does NOT modify research_notes or confidence_score
    #    (that's Critic's job — Fact Checker just flags, doesn't reject)
```

**Fact Checker prompt philosophy:**
- Skeptical but fair — flag genuinely dubious claims only
- Don't flag well-known facts or clearly sourced information
- Identify vague, unverifiable, contradictory, or hallucinated claims
- Output only the flagged list (no commentary)

**State schema changes:**
```python
class AgentState(TypedDict):
    # ... existing fields ...
    flagged_claims: list[str]   # ← NEW: list of flagged suspicious claims
    # ... rest of fields ...
```

**Graph position:** Between Researcher and Critic

---

## Branch: `origin/Presenter-Agent` (Sid)

**Last commit:** `e4322ac` — "Implement presenter agent with Groq + test harness" (4 weeks ago)

**Files modified:**
- `agents/presenter.py` ✨ NEW (fully implemented, not stub)
- `prompts/presenter_prompt.py` ✨ NEW (already existed, refined)

**What it does:**

The Presenter is the final node. It synthesizes all gathered research into a user-facing response.

```python
def presenter_node(state: AgentState) -> AgentState:
    # Uses Groq llama-3.3-70b-versatile, temperature=0.5 (balanced)
    # Input: state["user_input"], state["domain"], state["subtasks"], state["research_notes"]
    # Output: state["final_output"]
    
    # 1. Build research context block:
    #    Subtask 1: <subtask>
    #    Research: <research_note>
    #    
    #    Subtask 2: <subtask>
    #    Research: <research_note>
    #    ...
    # 2. Pass to LLM with system prompt
    # 3. LLM synthesizes into a polished, user-friendly response
    # 4. Write to state["final_output"]
```

**Presenter prompt philosophy:**
- Takes all the research and makes it coherent, narrative-friendly
- Preserves specificity (numbers, names, details from research)
- Addresses the original user request
- No longer lists research; synthesizes into flowing prose

**State changes:** None (writes to final_output)

**Test:** `tests/test_presenter.py` (mock state test, runs standalone)

---

## Summary: What's NOT Yet Built

1. **Memory Agent** — NOT on any branch yet
   - Should run BEFORE Planner: injects prior run context into state
   - Should run AFTER Presenter: saves run summary to persistent storage
   - Your (Sid's) responsibility

2. **tools/search.py** — Still stubs
   - `_tavily_search()` — needs Tavily client
   - `_wikipedia_search()` — needs wikipediaapi
   - Researcher depends on this; will crash if search is called but not implemented
   - Someone needs to implement; probably Bose4life since Researcher is his

3. **graph.py (final integration)** — Partially complete
   - `origin/researcher` has graph.py that includes Query Rewriter + Planner + Researcher + Critic + Presenter
   - Missing: Domain Router, Fact Checker, Memory Agent
   - Your responsibility to wire the full pipeline

---

## State Schema Reconciliation

Three branches touch `state.py`:
- `origin/researcher`: Adds `original_input` field
- `origin/fact_check`: Adds `flagged_claims` field
- Both need to be merged (they don't conflict on field names)

**Final merged state should have:**
```python
class AgentState(TypedDict):
    original_input: str          # from researcher branch
    user_input: str
    subtasks: list[str]
    domain: str
    research_notes: list[str]
    confidence_score: float
    critique: str
    iteration_count: int
    flagged_claims: list[str]    # from fact_check branch
    final_output: str
```

Plus your Memory Agent will add:
```python
    memory_context: str          # injected by Memory Agent at start
```

---

## Files Status Across Branches

| File | planner | researcher | critic | domain_router | fact_check | presenter |
|------|---------|------------|--------|---------------|------------|-----------|
| agents/planner.py | ✨ | — | — | — | — | — |
| agents/query_rewriter.py | — | ✨ | — | — | — | — |
| agents/researcher.py | — | ✨ | — | — | — | — |
| agents/critic.py | — | — | ✨ | — | — | — |
| agents/router.py | — | — | — | ✨ | — | — |
| agents/fact_checker.py | — | — | — | — | ✨ | — |
| agents/presenter.py | — | — | — | — | — | ✨ |
| prompts/planner_prompt.py | ✨ | — | — | — | — | — |
| prompts/query_rewriter_prompt.py | — | ✨ | — | — | — | — |
| prompts/researcher_prompt.py | — | ✨ | — | — | — | — |
| prompts/critic_prompt.py | — | — | ✨ | — | — | — |
| prompts/router_prompt.py | — | — | — | ✨ | — | — |
| prompts/fact_checker_prompt.py | — | — | — | — | ✨ | — |
| prompts/presenter_prompt.py | — | — | — | — | — | ✨ |
| state.py | — | 🔄 | — | — | 🔄 | — |
| graph.py | — | 🔄 | — | — | — | — |
| tools/search.py | — | — | — | — | — | — |

---

## Integration Path Forward

**Next steps (your responsibility):**

1. **Create `agents/memory_agent.py`** (new)
2. **Create `prompts/memory_agent_prompt.py`** (new)
3. **Update `state.py`** to merge researcher + fact_check + your memory_context
4. **Rewrite `graph.py`** to wire: query_rewriter → router → memory_agent_pre → planner → researcher → fact_checker → critic → [conditional] → presenter → memory_agent_post → END
5. **Implement `tools/search.py`** (or confirm Bose4life is doing it)
6. **Create integration test** in `tests/test_graph_integration.py`
7. **Merge all branches** into `integration` branch (cherry-picks, not merges, to preserve history)
8. **Test end-to-end**
9. **Merge `integration` → `main`**

All branches stay intact for reference in the final codebase.
