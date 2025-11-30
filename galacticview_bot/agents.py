from typing import TypedDict, Annotated, List

import json

from langgraph.prebuilt import ToolNode
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langgraph.graph import StateGraph, END

from .model import llm
from .search import tavily_search_tool
from .response_structure import SpaceResponseStructure


tools = [tavily_search_tool]
llm_with_tools = llm.bind_tools(tools)



class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], "add_messages"]


# Node functions

"""
Input: The State (specifically looking for the last message with a tool_calls request).

Action: It sees the Agent asked for a search. It actually calls the Tavily API.

Output: It returns a ToolMessage containing the raw text found on the internet.
"""
tool_node = ToolNode(tools)

def reasoner(state: AgentState):
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


def formatter(state: AgentState):
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
    structured_llm = llm.with_structured_output(SpaceResponseStructure)
    response = structured_llm.invoke(formatter_prompt)
    
    return {"messages": [HumanMessage(content=json.dumps(response.dict()))]}


# Edge conditions

def should_continue(state: AgentState):
    """
    Conditional logic: If tool calls exist, go to tools. Else, format output.
    """
    last_message = state["messages"][-1]

    # check if the last message has tool calls
    if last_message.tool_calls:
        return "tools" # go to tool node
    return "formatter" # go to formatter



# Agent graph
workflow = StateGraph(AgentState)

workflow.add_node("agent", reasoner)
workflow.add_node("tools", tool_node)
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