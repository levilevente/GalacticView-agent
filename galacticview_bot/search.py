import os
from dotenv import load_dotenv

load_dotenv()

try:
    from langchain_tavily import TavilySearch
    if os.getenv("TAVILY_API_KEY"):
        tavily_search_tool = TavilySearch(
            max_results=5,
            topic="general",
            include_answer=True,
            include_raw_content=False,
            description="Search the internet for space-related information and return relevant results.",
        )
    else:
        # No API key — create a stub that returns no results.
        class _StubSearch:
            def run(self, query: str):
                return []

        tavily_search_tool = _StubSearch()
except Exception:
    class _StubSearch:
        def run(self, query: str):
            return []

    tavily_search_tool = _StubSearch()