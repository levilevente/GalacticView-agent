from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import uvicorn

import os

from .service import chat_ask_question

from .dto import ChatTypeIn, ChatTypeOut

# get_remote_address uses the user's IP to track usage
limiter = Limiter(key_func=get_remote_address)


app = FastAPI()

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/chat")
@limiter.limit("7/minute")
def chat_endpoint(request: Request, body: ChatTypeIn) -> ChatTypeOut:
    """
    Process chat questions using the agent and return structured responses.
    Rate limited to 7 requests per minute per IP.
    """
    response_data: ChatTypeOut = chat_ask_question(body)
    return response_data

def main() -> None:
    """
    Main function to run the FastAPI app using Uvicorn.
    """
    env = os.getenv("ENVIRONMENT", "prod")
    
    reload = env == "dev"
    host = "127.0.0.1"
    if env == "prod":
        host = "0.0.0.0"

    uvicorn.run("server.serve:app", host=host, port=8000, reload=reload)

if __name__ == "__main__":
    main()