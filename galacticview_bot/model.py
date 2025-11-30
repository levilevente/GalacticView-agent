from dotenv import load_dotenv
import os

from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq
from langchain_core.language_models import BaseChatModel 


load_dotenv()

llm: BaseChatModel

if os.getenv("LLM_LOCAL", "True").lower() == "true":
    print("Using Local Model (Ollama)")
    MODEL_NAME = os.getenv("MODEL_NAME", "llama3.1")
    llm = ChatOllama(
      model=MODEL_NAME,
      temperature=0,
      top_k=20, 
      num_ctx=8192
    )
else:
    print("Using Cloud Model (Groq)")
    llm = ChatGroq(
        model="llama-3.1-8b-instant", 
        temperature=0
    )