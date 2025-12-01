from galacticview_bot import AgentApp
from .dto import ChatTypeIn, ChatTypeOut

from langchain_core.messages import SystemMessage, HumanMessage

import json

def chat_ask_question(chat_input: ChatTypeIn):
    """
    Function to ask a question to the agent and get a response.
    """
    question = chat_input.question

    sys_msg = SystemMessage(
        content="You are a friendly and knowledgeable space enthusiast. Provide detailed and accurate information about space-related topics, including key metrics where applicable."
    )

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

        for event in AgentApp.stream(inputs, config=config):  # type: ignore
            for key, value in event.items():
                if key == "formatter":
                    raw_json = value["messages"][0].content
                    response_data = ChatTypeOut(**json.loads(raw_json))
                    return response_data
                    
    except Exception as e:
        return {"error": str(e)}  
