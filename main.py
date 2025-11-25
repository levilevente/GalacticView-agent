import json
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from ddgs import DDGS 
from langchain_core.messages import AIMessage

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

schema_str = json.dumps(ResponseStructure.model_json_schema(), indent=2)

system_prompt = """
You are a Senior Aerospace Engineer.
Your goal is to provide accurate information about space.

PROTOCOL:
1. Call 'search_internet_for_text' to gather facts.
2. Call 'search_internet_for_images' to find images.
3. Finally, output a JSON object that strictly matches this schema:

{schema_str}

CRITICAL RULES:
- The keys MUST be exactly "title", "content", and "images".
- Do NOT invent new keys like "name" or "description".
- The "content" field must be a detailed summary of the text search results.
- Output ONLY the JSON. No other text.
"""

graph = create_agent(
    model=model,
    tools=tools,
    response_format=ToolStrategy(ResponseStructure),
    system_prompt=system_prompt,
    debug=False,
)

if __name__ == "__main__":
    while True:
        question = input("Enter your space-related question (quit/exit to quit): ")

        if question.lower() in {"exit", "quit"}:
            print("Exiting the program.")
            break
        
        input_data = {"messages": [("user", question)]}
        response = graph.invoke(input_data)

        print("[DEBUG] Full Response Object:")
        print(response)
        
        print("🪐 Final Structured Output:")

        output_data = None
        if "structured_response" not in response:
            last_ai = next(m for m in reversed(response["messages"]) if isinstance(m, AIMessage))
            content = last_ai.content
            print("[DEBUG] Raw JSON Content:")
            print(content)
            output_data = json.loads(content)
            print("Title:", output_data["title"])
            print("Content:", output_data["content"])
            print("Images:")
            for img in output_data["images"]:
                print(img)
        else:
            output_data = response["structured_response"]
            print("Title:", output_data.title)
            print("Content:", output_data.content)
            print("Images:")
            for img in output_data.images:
                print(f" - {img['title']}: {img['url']}")

