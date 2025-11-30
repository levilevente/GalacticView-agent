from dotenv import load_dotenv
import os
from langchain_ollama import ChatOllama

from langchain_groq import ChatGroq

load_dotenv()


if os.getenv("LLM_LOCAL", "True").lower() == "true":
    MODEL_NAME = os.getenv("MODEL_NAME", "llama3.1")
    llm = ChatOllama(
      model=MODEL_NAME,
      temperature=0,
      top_k=20,
      seed=42,
      num_ctx=8192
    )
else:
    llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)