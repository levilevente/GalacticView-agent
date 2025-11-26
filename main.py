import json
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from ddgs import DDGS 
from langchain_core.messages import AIMessage


from langchain.agents import create_agent, AgentState
from pydantic import BaseModel, Field
from langchain.agents.structured_output import ToolStrategy


class ResponseStructure(BaseModel):
    title: str = Field(description="A catchy title for the topic")
    content: str = Field(description="A detailed summary of the topic")
    images: list[dict[str, str]] = Field(description="A list of image results with URLs and titles")

model = ChatOllama(model="llama3.1", temperature=0, top_k=5, seed=42)

@tool
def search_internet_for_text(query: str):
    """Searches the internet for real-time information."""

    print(f"  🔎 Searching text for: {query}")
    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=5)
            if not results:
                return "No text results found."
            summary = " ".join([result.get("body", "") for result in results])
            return summary
    except Exception as e:
        print(f"Error detail: {e}")
        return f"Error searching text: {e}"    
@tool
def search_internet_for_images(query: str):
    """Searches the internet for images. Returns a list of image URLs."""

    print(f"  📸 Searching images for: {query}")
    try:
        with DDGS() as ddgs:
            results = ddgs.images(query, max_results=4)
        if not results:
            return "No image results found."
        return results
    except Exception as e:
        print(f"Error detail: {e}")
        return f"Error searching images: {e}"
    

tools = [search_internet_for_text, search_internet_for_images]

class CustomState(AgentState):
    user_preferences: dict



schema_str = json.dumps(ResponseStructure.model_json_schema(), indent=2)

system_prompt = """
You are a Senior Aerospace Engineer.

PROTOCOL:
1. Call 'search_internet_for_text' to gather facts.
2. Call 'search_internet_for_images' to find images.
3. Output a JSON object matching this schema:

{schema_str}

CRITICAL RULES:
- The 'content' must ANSWER THE USER'S QUESTION. 
- Do not just summarize the search results if they are irrelevant to the specific question.
- If the search results are bad (e.g., discussing distance instead of star count), use your INTERNAL KNOWLEDGE to correct it.
- The keys MUST be exactly "title", "content", and "images".
- Output ONLY the JSON.
"""


system_prompt_2 = """
    You are a Weather Information Specialist.
"""

graph = create_agent(
    model=model,
    tools=tools,
    response_format=ToolStrategy(ResponseStructure),
    system_prompt=system_prompt,
    debug=False,
    state_schema=CustomState
)

if __name__ == "__main__":
    while True:
        question = input("Enter your space-related question (quit/exit to quit): ")

        if question.lower() in {"exit", "quit"}:
            print("Exiting the program.")
            break
        
        input_data = {"messages": [("user", question)], "user_preferences": {"style": "technical", "verbosity": "detailed"}}
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
            