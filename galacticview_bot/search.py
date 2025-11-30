import os
from dotenv import load_dotenv

from langchain_tavily import TavilySearch
from pydantic import BaseModel, Field

load_dotenv()

class TavilyInput(BaseModel):
    query: str = Field(description="The search query")

if os.getenv("TAVILY_API_KEY"):
    tavily_search_tool = TavilySearch(
        max_results=3,
        topic="general",
        include_answer=True,
        include_raw_content=False,
        args_schema=TavilyInput,
        description="Search the internet for space-related information and return relevant results.",
    )
else:
    if __name__ == "__main__":
        print("WARNING: TAVILY_API_KEY not set. Tavily search tool will be disabled.")