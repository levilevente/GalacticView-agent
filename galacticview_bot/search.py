import os
from dotenv import load_dotenv

from langchain_tavily import TavilySearch

load_dotenv()

if os.getenv("TAVILY_API_KEY"):
    tavily_search_tool = TavilySearch(
        max_results=5,
        topic="general",
        include_answer=True,
        include_raw_content=False,
        description="Search the internet for space-related information and return relevant results.",
    )
else:
    print("[WARNING] TAVILY_API_KEY not found in environment variables. Using stub search tool.")