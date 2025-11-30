from typing import TypedDict, Annotated, List

import json

from langchain_core.messages import BaseMessage, ToolMessage, HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages

from .model import llm
from .search import tavily_search_tool
from .response_structure import SpaceResponseStructure

tools = [tavily_search_tool]

llm_with_tools = llm.bind_tools(tools)

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]    

# Node functions

def custom_tool_node(state: AgentState) -> AgentState:
    """
    A tool node that executes the requested tool calls.

    Input: The State (specifically looking for the last message with a tool_calls request).

    Action: It sees the Agent asked for a search. It actually calls the Tavily API.

    Output: It returns a ToolMessage containing the raw text found on the internet.
    """

    message = state["messages"]
    last_message = message[-1]

    tool_calls = getattr(last_message, "tool_calls", [])
    
    if not tool_calls:
        return {"messages": []}
    
    tool_map = {tool.name: tool for tool in tools}

    results = []

    for tool_call in tool_calls:
        tool_name = tool_call['name']
        tool_args = tool_call['args']
        tool_call_id = tool_call['id']

        print(f"Executing Custom Tool: {tool_name} with args: {tool_args}")

        if tool_name in tool_map:
            

            try:
                chosen_tool = tool_map[tool_name]

                raw_output = chosen_tool.invoke(tool_args)

                if not raw_output:
                    print(f"WARNING: Tool returned EMPTY result for query: {tool_args.get('query')}")
                    clean_content = "Search returned no results. Try a broader query without filters."
                else:
                    print(f"Tool returned data (Length: {len(str(raw_output))})")
                    clean_content = json.dumps(raw_output) if isinstance(raw_output, (dict, list)) else str(raw_output) 
            except Exception as e:
                clean_content = f"Error executing tool {tool_name}: {e}"
        else:
            print(f"Tool {tool_name} not found.")
            clean_content = f"Error: Tool {tool_name} not found."
        
        results.append(ToolMessage(
            tool_call_id=tool_call_id,
            content=str(clean_content),
            name=tool_name
        ))

    # unnecessary suppression of type checker here
    return {"messages": results} # type: ignore


def reasoner(state: AgentState) -> AgentState:
    """
    The brain. Decides whether to search or answer.

    Input: The current conversation history.

    Action: It sends the history to the LLM.

    Output: It returns an AIMessage. This message might contain text
            ("Here is the answer...") OR it might contain a tool_calls request.
    """
    messages = state["messages"]

    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}


def formatter(state: AgentState) -> AgentState:
    """
    Takes the final raw text conversation and forces it into the JSON schema.

    Input: The raw answer text from the Agent.

    Action: It runs a separate LLM call (or the same one with different instructions) specifically to clean up the messy text into your SpaceResponseStructure JSON.

    Output: A clean JSON string.
    """
    messages = state["messages"]
    
    # a specific system prompt for the formatting step
    formatter_prompt = [
        SystemMessage(content="You are a data extractor. Convert the conversation history into the specific JSON schema provided."),
        messages[-1] # the last message contains the raw answer found by the agent
    ]
    
    # force structured output
    schema_constrained_llm = llm.with_structured_output(SpaceResponseStructure.model_json_schema())
    response = schema_constrained_llm.invoke(formatter_prompt)
    
    return {"messages": [HumanMessage(content=json.dumps(response))]}


# Edge conditions

def should_continue(state: AgentState) -> str:
    """
    Conditional logic: If tool calls exist, go to tools. Else, format output.
    """
    messages = state["messages"]
    last_message = messages[-1]

    
    tool_calls = getattr(last_message, "tool_calls", [])
    
    if not tool_calls:
        return "formatter"
    ai_moves = len([m for m in messages if m.type == "ai"])

    if ai_moves >= 5:
        print("STOP: Maximum reasoning steps reached. Forcing format.")
        return "formatter"
    
    return "tools"

# Agent graph
workflow = StateGraph(AgentState)

workflow.add_node("agent", reasoner)
workflow.add_node("tools", custom_tool_node)
workflow.add_node("formatter", formatter)

workflow.set_entry_point("agent")

workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        "formatter": "formatter",
    },
)

workflow.add_edge("tools", "agent") # loop back to agent after using tool
workflow.add_edge("formatter", END)


app = workflow.compile()