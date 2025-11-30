from dotenv import load_dotenv
import os
from langchain_ollama import ChatOllama


load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME", "llama3.1")

llm = ChatOllama(
  model=MODEL_NAME,
  temperature=0,
  top_k=20,
  seed=42,
  num_ctx=8192
)


