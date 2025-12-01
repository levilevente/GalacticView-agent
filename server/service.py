from galacticview_bot import app, sys_msg
from .dto import ChatTypeIn, ChatTypeOut

from langchain_core.messages import SystemMessage, HumanMessage

import json

def chat_ask_question(chat_input: ChatTypeIn) -> ChatTypeOut:
    """
    Function to ask a question to the agent and get a response.
    """
    question = chat_input.question

    inputs = {"messages": [sys_msg, HumanMessage(content=question)]}

    response_data: ChatTypeOut = ChatTypeOut(
        title="",
        content="",
        key_metrics=[]
    )

    try:
        thread_id = "aerospace-agent-thread-001"

        config = {
            "configurable": {"thread_id": thread_id},
            "recursion_limit": 50
        }

        for event in app.stream(inputs, config=config):  # type: ignore
            for key, value in event.items():
                if key == "formatter":
                    raw_json = value["messages"][0].content
                    response_data = ChatTypeOut(**json.loads(raw_json))
                    return response_data
                    
    except Exception as e:
        return ChatTypeOut(title="Error", content="Error occurred while processing the request.", key_metrics=[])  
    
    return response_data
