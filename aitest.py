from dotenv import load_dotenv
from langchain_ollama import ChatOllama

load - load_dotenv('./../.env')

llm = ChatOllama(
    model="gemini-3-pro-preview:latest", 
    base_url="http://localhost:11434",
    temperature=0.5,
    max_retries=3,
    max_tokens=2048
)