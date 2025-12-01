from fastapi import FastAPI
import uvicorn

from .service import chat_ask_question

from .dto import ChatTypeIn, ChatTypeOut

app = FastAPI()

@app.get("/")
def read_root() -> dict[str, str]:
    """
    A simple root endpoint.
    """
    return {"Hello": "World"}

@app.post("/chat")
def chat_endpoint(request: ChatTypeIn) -> ChatTypeOut:
    """
    A placeholder chat endpoint that would interact with the agent.
    """
    response_data: ChatTypeOut = chat_ask_question(request)
    return response_data


def main() -> None:
    """
    Main function to run the FastAPI app using Uvicorn.
    """
    uvicorn.run("server.serve:app", host="0.0.0.0", port=8000, reload=True)

    
if __name__ == "__main__":
    main()