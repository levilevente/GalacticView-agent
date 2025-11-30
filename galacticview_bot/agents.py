from typing import TypedDict, Annotated, List

import json

from langchain_core.messages import BaseMessage, ToolMessage, HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END

from .model import llm
from .search import tavily_search_tool
from .response_structure import SpaceResponseStructure


tools = [tavily_search_tool]
llm_with_tools = llm.bind_tools(tools)



class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], "add_messages"]


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

    if isinstance(last_message, ToolMessage):
        tool_calls = last_message.tool_calls # type: ignore
    else:
        tool_calls = getattr(last_message, "tool_calls", None) or []

    if not tool_calls:
        return state  # No tool calls to process
    
    tool_map = {tool.name: tool for tool in tools}

    results = []

    for tool_call in tool_calls:
        tool_name = tool_call['name']
        tool_args = tool_call['args']
        tool_call_id = tool_call['id']

        print(f"  🛠️ Executing Custom Tool: {tool_name} with args: {tool_args}")

        if tool_name in tool_map:
            chosen_tool = tool_map[tool_name]

            raw_output = chosen_tool.invoke(tool_args)

            try:
                clean_content = json.dumps(raw_output, default=str)
            except Exception as e:
                clean_content = f"Error executing tool {tool_name}: {e}"
        else:
            print(f"  ⚠️ Tool {tool_name} not found.")
            clean_content = f"Error: Tool {tool_name} not found."
        
        results.append(ToolMessage(
            tool_call_id=tool_call_id,
            content=str(clean_content),
            name=tool_name
        ))

    return {"messages": state["messages"] + results} # type: ignore



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
    structured_llm = llm.with_structured_output(SpaceResponseStructure.model_json_schema())
    response = structured_llm.invoke(formatter_prompt)
    
    return {"messages": [HumanMessage(content=json.dumps(response))]}


# Edge conditions

def should_continue(state: AgentState) -> str:
    """
    Conditional logic: If tool calls exist, go to tools. Else, format output.
    """
    last_message = state["messages"][-1]

    tool_calls = getattr(last_message, "tool_calls", None)
    if tool_calls:
        return "tools"  # go to tool node
    return "formatter" # go to formatter


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

workflow.add_edge("tools", "agent") # Loop back to agent after using tool
workflow.add_edge("formatter", END)


app = workflow.compile()