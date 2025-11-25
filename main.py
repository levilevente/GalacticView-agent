from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from ddgs import DDGS 

from langchain.agents import create_agent
from pydantic import BaseModel, Field
from langchain.agents.structured_output import ToolStrategy

model = ChatOllama(model="llama3.1", temperature=0)

@tool
def search_internet_for_text(query: str):
    """Searches the internet for real-time information."""

    print(f"  🔎 Searching text for: {query}")
    try:
        results = DDGS().text(query, max_results=2)
        if not results:
            return "No text results found."
        return results
    except Exception as e:
        print(f"Error detail: {e}")
        return f"Error searching text: {e}"
    
@tool
def search_internet_for_images(query: str):
    """Searches the internet for images. Returns a list of image URLs."""

    print(f"  📸 Searching images for: {query}")
    try:
        results = DDGS().images(query, max_results=4)
        if not results:
            return "No image results found."
        return results
    except Exception as e:
        print(f"Error detail: {e}")
        return f"Error searching images: {e}"
    

tools = [search_internet_for_text, search_internet_for_images]

class ResponseStructure(BaseModel):
    title: str = Field(description="A catchy title for the topic")
    content: str = Field(description="A detailed summary of the topic")
    images: list[dict[str, str]] = Field(description="A list of image results with URLs and titles")

system_prompt = """
You are a Senior Aerospace Engineer.
Your goal is to provide accurate information about space.

PROTOCOL:
1. FIRST, use 'search_internet_for_text' to gather facts.
2. SECOND, use 'search_internet_for_images' to find relevant visuals.
3. FINALLY, compile all data into the Structured Output format.

CRITICAL: You MUST return the result as a Structured Output. Do not just reply with text.
"""

graph = create_agent(
    model=model,
    tools=tools,
    response_format=ToolStrategy(ResponseStructure),
    system_prompt=system_prompt,
    debug=True,
)

if __name__ == "__main__":
    print("-" * 20)
    question = input("Enter your space-related question: ")
    print("-" * 20)
    input = {"messages": [("user", question)]}
    response = graph.invoke(input)
    print("🪐 Final Structured Output:")
    print(response["structured_response"])

    print("Title:", response["structured_response"].title)
    print("Content:", response["structured_response"].content)
    print("Images:")
    for img in response["structured_response"].images:
        print(f" - {img['title']}: {img['url']}")