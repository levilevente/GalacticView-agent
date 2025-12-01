from fastapi import FastAPI
import uvicorn

from dotenv import load_dotenv
import os

from .service import chat_ask_question

from .dto import ChatTypeIn, ChatTypeOut

app = FastAPI()

@app.post("/chat")
def chat_endpoint(request: ChatTypeIn) -> ChatTypeOut:
    """
    Process chat questions using the agent and return structured responses.
    """
    response_data: ChatTypeOut = chat_ask_question(request)
    return response_data


def main() -> None:
    """
    Main function to run the FastAPI app using Uvicorn.
    """
    load_dotenv()

    reload = os.getenv("ENVIRONMENT", "prod") == "dev"
    uvicorn.run("server.serve:app", host="127.0.0.1", port=8000, reload=reload)

    
if __name__ == "__main__":
    main()