from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from pathlib import Path

# Load env variables
load = load_dotenv(".env")
FilePath = Path(__file__).parent / "secure_prompt.txt"

with open(FilePath, "r", encoding="utf-8") as f:
    secure_prompt = f.read().strip()

# Initialize LLM with system prompt
llm = ChatOllama(
    #model="llama3.2:3b",
    model="deepseek-v3.2:cloud",
    base_url="http://localhost:11434",
    temperature=0.5,
    max_retries=3,
    max_tokens=2048,
    system=secure_prompt
)

response = llm.invoke("Explain OAuth2 in one paragraph")
print(response.content)