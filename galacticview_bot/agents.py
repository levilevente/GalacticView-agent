from langchain.agents import create_agent, AgentState
from langchain.agents.structured_output import ToolStrategy

class CustomState(AgentState):
    user_preferences: dict

def space_agent_graph(model, tools, system_prompt, ResponseStructure):
  return create_agent(
    model=model,
    tools=tools,
    response_format=ToolStrategy(ResponseStructure),
    system_prompt=system_prompt,
    debug=False,
    state_schema=CustomState
  )
