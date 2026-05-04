# AGI-Simulation

A multi-agent pipeline built with LangGraph and Groq that simulates AGI-like reasoning through collaborative agent specialization. Developed as the final project for Seminar Topics in Computer Science at Temple University.

## Overview

The central argument of this project is that multi-agent systems can exhibit proto-AGI capabilities — not through a single monolithic model, but through specialized agents collaborating, self-correcting, and accumulating knowledge over time.

The pipeline takes a raw user query, refines it, routes it by domain, plans a research strategy, gathers and fact-checks information, evaluates quality, and synthesizes a final response. A memory layer persists context across sessions.

## Architecture

```
User Input
    ↓
[Query Rewriter]     — cleans and clarifies vague or messy input
    ↓
[Domain Router]      — classifies query into medical / scientific / legal / financial / travel / general
    ↓
[Memory Agent PRE]   — injects context from prior runs before planning begins
    ↓
[Planner]            — breaks the query into 3–5 concrete research subtasks
    ↓
[Researcher]         — gathers information per subtask via search + LLM synthesis
    ↓
[Fact Checker]       — flags unverifiable or contradictory claims in research output
    ↓
[Critic]             — scores research quality (0.0–1.0); loops back to Researcher if score < 0.7
    ↓
[Presenter]          — synthesizes all research into a final user-facing response
    ↓
[Memory Agent POST]  — saves a one-sentence summary of the run to persistent memory
    ↓
Final Output
```

The Critic → Researcher loop runs up to 3 times before proceeding regardless of score.

## Agents

| Agent | Owner | File |
|---|---|---|
| Query Rewriter | Bose4life | `agents/query_rewriter.py` |
| Domain Router | Luke | `agents/router.py` |
| Memory Agent | Sid | `agents/memory_agent.py` |
| Planner | Hamza | `agents/planner.py` |
| Researcher | Bose4life | `agents/researcher.py` |
| Fact Checker | Hamza | `agents/fact_checker.py` |
| Critic | Luke | `agents/critic.py` |
| Presenter | Sid | `agents/presenter.py` |

## Tech Stack

- **LangGraph** — agent graph orchestration
- **Groq** — LLM inference (llama-3.3-70b-versatile)
- **LangChain** — LLM interface layer
- **Tavily** — web search (optional)
- **Wikipedia API** — search fallback (no key required)
- **Python 3.11**

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/NightmareHel/AGI-Simulation.git
cd AGI-Simulation
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Configure environment variables**

Create a `.env` file in the project root:
```
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here   # optional — omit to use Wikipedia fallback
```

Get a free Groq API key at [console.groq.com](https://console.groq.com).

## Running

**Single query:**
```bash
python main.py "What are the treatment options for type 2 diabetes?"
```

**Interactive mode:**
```bash
python main.py
```

## Tests

**Full pipeline (all 7 domains):**
```bash
python tests/test_integration.py
```
Writes one log file per query to `logs/log#.txt`.

**Isolated agent tests:**
```bash
python tests/test_presenter.py
python tests/test_memory_agent.py
python tests/test_researcher.py
python test_critic.py
python test_router.py
```

## Memory

The Memory Agent persists run summaries to `memory/runs.jsonl` (gitignored). On each new run, the last 3 summaries are injected into the query before the Planner sees it, giving the system cross-session context.

To reset memory before a demo:
```bash
> memory/runs.jsonl
```

## Logs

Test run outputs are saved to `logs/log#.txt`. Each log contains the original query, rewritten query, domain classification, memory context injected, subtasks, flagged claims, confidence score, iteration count, and final output.

## Project Structure

```
AGI-Simulation/
├── agents/          — one file per agent
├── prompts/         — system prompts for each agent
├── tools/           — search tool (Tavily + Wikipedia)
├── tests/           — isolated and integration tests
├── logs/            — test run output logs
├── memory/          — persistent run summaries (gitignored)
├── graph.py         — LangGraph pipeline definition
├── state.py         — shared AgentState schema
├── main.py          — CLI entry point
└── requirements.txt
```

## Team

| Name | Role |
|---|---|
| Sid Kumar | Memory Agent, Presenter, Graph Integration |
| Hamza Malik | Planner, Fact Checker |
| Bose4life | Researcher, Query Rewriter |
| Luke Immel | Critic, Domain Router |
