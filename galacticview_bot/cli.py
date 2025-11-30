import json
import datetime

from langchain_core.messages import SystemMessage, HumanMessage

from .agents import app

def main() -> int:
    print("🚀 Aerospace Agent Online (Tavily + LangGraph)")

    # Example prompt for a quick smoke run; in interactive mode you'll want to
    # replace this with user input or an API endpoint.
    user_q = "What is the latest news about the Artemis mission?"

    # Initial System Prompt to set persona
    sys_msg = SystemMessage(
        content="You are a friendly and knowledgeable space enthusiast. Provide detailed and accurate information about space-related topics, including key metrics where applicable."
        )

    inputs = {"messages": [sys_msg, HumanMessage(content=user_q)]}

    # Stream events to see it thinking
    try:
        thread_id =  "aerospace-agent-thread-001"

        config = {
            "configurable": {"thread_id": thread_id},
            "recursion_limit": 50 
        }

        for event in app.stream(inputs, config=config):
            for key, value in event.items():
                print(f"\n--- Node: {key} ---")
                # In the formatter node, we can grab the final JSON
                if key == "formatter":
                    raw_json = value["messages"][0].content
                    data = json.loads(raw_json)
                    print("\n🪐 FINAL OUTPUT:")
                    print(json.dumps(data, indent=2))
    except Exception as e:
        print(f"Error while running agent: {e}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

