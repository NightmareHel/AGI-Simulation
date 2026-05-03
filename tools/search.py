import os


def run_search(query: str) -> str:
    """
    Runs a search for the given query. Returns results as a plain string.
    Uses Tavily if TAVILY_API_KEY is set, otherwise falls back to Wikipedia.
    """
    tavily_key = os.getenv("TAVILY_API_KEY")
    if tavily_key:
        return _tavily_search(query, tavily_key)
    return _wikipedia_search(query)


def _tavily_search(query: str, api_key: str) -> str:
    from tavily import TavilyClient
    client = TavilyClient(api_key=api_key)
    response = client.search(query, max_results=5)
    return "\n\n".join(r["content"] for r in response.get("results", []))


def _wikipedia_search(query: str) -> str:
    import wikipediaapi
    wiki = wikipediaapi.Wikipedia("AGI-Simulation-Agent/1.0", "en")
    page = wiki.page(query)
    if page.exists():
        return page.summary
    return ""
