from langchain_tavily import TavilySearch
from dotenv import load_dotenv
import os

load_dotenv()

if not os.getenv("TAVILY_API_KEY"):
    raise ValueError("TAVILY_API_KEY not found in environment variables.")

tavily_search_tool = TavilySearch(
    max_results=5,
    topic="general",
    include_answer=True,
    include_raw_content=False,
    description="Search the internet for space-related information and return relevant results.",
)

print("Tavily search tool initialized.")