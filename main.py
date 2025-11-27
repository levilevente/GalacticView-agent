import json
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from agents import space_agent_graph
from ddgs import DDGS 
from langchain_core.messages import AIMessage
from response_structure import TextAndImageStructure, TextResponseStructure
from tools import search_internet_for_text, search_internet_for_images


from langchain.agents import create_agent, AgentState
from pydantic import BaseModel, Field
from langchain.agents.structured_output import ToolStrategy

model = ChatOllama(model="llama3.1", temperature=0, top_k=5, seed=42)

tools = [search_internet_for_text, search_internet_for_images]

schema_str = json.dumps(TextResponseStructure.model_json_schema(), indent=2)

system_prompt = f"""
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
You are a Senior Aerospace Engineer.

PROTOCOL:
1. Call 'search_internet_for_text' to gather facts.
2. Output a JSON object matching this schema:

{schema_str}

CRITICAL RULES:
- The 'content' must ANSWER THE USER'S QUESTION, in a detailed manner.
- Do not just summarize the search results if they are irrelevant to the specific question.
- If the search results are bad (e.g., discussing distance instead of star count), use your INTERNAL KNOWLEDGE to correct it.
- The keys MUST be exactly "title" and "content".
- Output ONLY the JSON.
"""

graph = space_agent_graph(model, tools, system_prompt_2, TextResponseStructure)

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
            if "images" in output_data:
                print("Images:")
                for img in output_data["images"]:
                    print(img)
        else:
            output_data = response["structured_response"]
            print("Title:", output_data.title)
            print("Content:", output_data.content)
            if hasattr(output_data, 'images'):
                print("Images:")
                for img in output_data.images:
                    print(f" - {img['title']}: {img['url']}")
            