import json

from langchain_core.messages import HumanMessage

from galacticview_bot.agents import app
from .system_messages import sys_msg

from loguru import logger

def main() -> int:
    print("Aerospace Agent Online (Tavily + LangGraph)")

    # example prompt for a quick smoke run; in interactive mode you'll want to
    # replace this with user input or an API endpoint.
    user_q = "What is the latest news about the Artemis mission?"


    inputs = {"messages": [sys_msg, HumanMessage(content=user_q)]}

    # stream events to see it thinking
    try:
        thread_id =  "aerospace-agent-thread-001"

        config = {
            "configurable": {"thread_id": thread_id},
            "recursion_limit": 50 
        }

        for event in app.stream(inputs, config=config): # type: ignore
            for key, value in event.items():
                print(f"\n--- Node: {key} ---")
                # in the formatter node, we can grab the final JSON
                if key == "formatter":
                    raw_json = value["messages"][0].content
                    data = json.loads(raw_json)
                    print("\nFINAL OUTPUT:")
                    print(json.dumps(data, indent=2))
    except Exception as e:
        logger.error(f"Error while running agent: {e}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

