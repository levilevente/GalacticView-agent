from galacticview_bot import app, sys_msg
from .dto import ChatTypeIn, ChatTypeOut

from loguru import logger

from langchain_core.messages import HumanMessage

import json
import uuid

def chat_ask_question(chat_input: ChatTypeIn) -> ChatTypeOut:
    """
    Function to ask a question to the agent and get a response.
    """
    question = chat_input.question

    inputs = {"messages": [sys_msg, HumanMessage(content=question)]}

    try:
        thread_id = f"aerospace-agent-thread-{uuid.uuid4()}"

        config = {
            "configurable": {"thread_id": thread_id},
            "recursion_limit": 50
        }

        for event in app.stream(inputs, config=config):  # type: ignore
            for key, value in event.items():
                if key == "formatter":
                    json_str = value["messages"][0].content
                    try:
                        response_data = ChatTypeOut(**json.loads(json_str))
                        return response_data
                    except json.JSONDecodeError:
                        return ChatTypeOut(title="Error", content="Malformed JSON received from formatter node.", key_metrics=[])
                    
    except Exception as e:
        logger.exception(f"Error occurred while processing the chat question. More details: {e}")
        return ChatTypeOut(title="Error", content="Error occurred while processing the request.", key_metrics=[])  
    
    return ChatTypeOut(title="Error", content="No response generated from the agent.", key_metrics=[])

