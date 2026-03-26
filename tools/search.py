"""
tools/search.py — Search Tool Wrapper

This file provides the run_search() function used by the Researcher agent to
gather external information. It abstracts over the search backend so you can
swap providers without touching the agent code.

What goes here:
- run_search(query: str) -> str
  Takes a plain-text query, returns a string of search results the LLM can read
- Backend selection logic — check for TAVILY_API_KEY in env; fall back to Wikipedia

Backends:

1. Tavily (preferred)
   - pip install tavily-python
   - Set TAVILY_API_KEY in your .env file
   - Returns clean, LLM-optimized search results
   - Free tier: ~1000 searches/month
   - Docs: https://docs.tavily.com

2. Wikipedia (fallback)
   - pip install wikipedia-api
   - No API key required
   - Good enough for research summaries and general knowledge
   - Not great for real-time or travel-specific data

What to implement:
1. Try to import the Tavily client; if TAVILY_API_KEY is set, use it
2. Otherwise, use the Wikipedia API to search and return the first section of the top result
3. Both paths should return a plain string (not JSON, not a list)
4. Handle exceptions gracefully — if search fails, return an empty string and log a warning

Usage in researcher.py:
    from tools.search import run_search
    results = run_search("best hotels in Tokyo under $150/night")

Environment variables needed:
- TAVILY_API_KEY (optional — falls back to Wikipedia if missing)
"""

import os


def run_search(query: str) -> str:
    """
    Runs a search for the given query string. Returns results as a plain string.
    Falls back to Wikipedia if Tavily key is not set.
    """
    tavily_key = os.getenv("TAVILY_API_KEY")

    if tavily_key:
        return _tavily_search(query, tavily_key)
    else:
        return _wikipedia_search(query)


def _tavily_search(query: str, api_key: str) -> str:
    """
    Uses the Tavily API to run a search. Returns results as a concatenated string.
    Requires: pip install tavily-python
    """
    # TODO: from tavily import TavilyClient
    # TODO: client = TavilyClient(api_key=api_key)
    # TODO: response = client.search(query, max_results=5)
    # TODO: extract and join result["content"] fields into a single string
    # TODO: return the joined string

    raise NotImplementedError("Implement _tavily_search")


def _wikipedia_search(query: str) -> str:
    """
    Uses the Wikipedia API as a free fallback. Returns the summary of the top result.
    Requires: pip install wikipedia-api
    """
    # TODO: import wikipediaapi
    # TODO: wiki = wikipediaapi.Wikipedia("AGI-Simulation-Agent/1.0", "en")
    # TODO: page = wiki.page(query)
    # TODO: if page.exists(): return page.summary
    # TODO: else: return ""

    raise NotImplementedError("Implement _wikipedia_search")
