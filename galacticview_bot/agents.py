from typing import Any, Sequence, Type

from langchain.agents import create_agent, AgentState
from langchain.agents.structured_output import ToolStrategy


class CustomState(AgentState):
    user_preferences: dict


def space_agent_graph(
    model: Any,
    tools: Sequence[Any],
    system_prompt: str,
    ResponseStructure: Type[Any],
) -> Any:
    """Create and return an agent graph configured with the provided model,
    tools and response schema.
    """
    return create_agent(
        model=model,
        tools=tools,
        response_format=ToolStrategy(ResponseStructure),
        system_prompt=system_prompt,
        debug=False,
        state_schema=CustomState,
    )
