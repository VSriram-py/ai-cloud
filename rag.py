from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from pathlib import Path
import sys
from utils import is_prompt_leak_attempt, detect_violation, handle_model_error

load_dotenv(".env")

EXIT_COMMANDS = {"done", "exit", "quit", "q"}

# Load secure prompt
FilePath = Path(__file__).parent / "secure_prompt.txt"
with open(FilePath, "r", encoding="utf-8") as f:
    secure_prompt = f.read().strip()

# Initialize LLM
llm = ChatOllama(
    model="qwen3-vl:235b-cloud",
    base_url="http://localhost:11434",
    temperature=0.5,
    max_tokens=250,
    system=secure_prompt
)

def get_text(response):
    if hasattr(response, "content"):
        return response.content
    return str(response)

def build_prompt(user_input: str, context: str = "") -> str:
    if context:
        return f"{secure_prompt}\n\nContext:\n{context}\n\nUSER PROMPT:\n{user_input}"
    return f"{secure_prompt}\n\nUSER PROMPT:\n{user_input}"

print("\nInteractive AI Console")
print("Type your prompt. Type 'quit', 'exit', 'done', or 'q' to leave.\n")

while True:
    try:
        user_input = input(">>> ").strip()
        if not user_input:
            continue
        if user_input.lower() in EXIT_COMMANDS:
            print("\nExiting! Goodbye.")
            sys.exit(0)

        if is_prompt_leak_attempt(user_input):
            print("\nPrompt rejected: access to system instructions is forbidden.\n")
            continue

        prompt = build_prompt(user_input)

        response = llm.invoke(prompt)
        response_text = get_text(response)

        if detect_violation(response_text):
            print("\nPrompt rejected due to policy violation.\n")
        else:
            print("\nResponse:\n")
            print(response_text)
            print("\n" + "-" * 60)

    except KeyboardInterrupt:
        print("\n\nInterrupted. Exiting.")
        sys.exit(0)

    except Exception as e:
        if handle_model_error(e):
            continue
        print("\nUnexpected error:")
        print(str(e))
        print("-" * 60)
