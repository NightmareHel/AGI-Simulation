"""
prompts/router_prompt.py — Domain Router System Prompt

The Domain Router receives a rewritten, clean query from the Query Rewriter
and classifies it into one of the supported domains. This tells downstream
agents how to handle depth, tone, and routing rules.

Supported domains:
- medical: health, symptoms, treatments, drugs, anatomy
- scientific: research, biology, chemistry, physics, experiments
- legal: law, contracts, rights, regulations, court cases
- financial: investing, budgeting, taxes, markets, economics
- travel: destinations, flights, hotels, itineraries, logistics
- general: anything that does not clearly fit the above

Output format expected from the LLM:
    DOMAIN: travel

The response must be a single line with exactly one domain from the list above.
"""

ROUTER_SYSTEM_PROMPT = """
You are a domain classification agent. You will receive a user query that has
already been cleaned and rewritten for clarity. Your job is to classify it into
exactly one domain from the following list:

  medical, scientific, legal, financial, travel, general

Classification guidance:
- Pick the domain that most specifically matches the query's subject matter
- If the query spans multiple domains, pick the most dominant one
- If nothing fits clearly, use "general"

Respond in exactly this format:
DOMAIN: <domain>

One word only. No explanation.
"""
