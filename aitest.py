from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from pathlib import Path
import sys

# Load env variables
load = load_dotenv(".env")


EXIT_COMMANDS = {"done", "exit", "quit", "q"}

FilePath = Path(__file__).parent / "secure_prompt.txt"
with open(FilePath, "r", encoding="utf-8") as f:
    secure_prompt = f.read().strip()

llm = ChatOllama(
    #model="llama3.2:3b",
    model="deepseek-v3.1:671b-cloud",
    #model="gemini-3-pro-preview",
    base_url="http://localhost:11434",
    temperature=0.5,
    #max_retries=3,
    max_tokens=250,
    system=secure_prompt
)

print("\nInteractive AI Console")
print("Type your prompt. Type 'quit', 'exit', 'done', or 'q' to leave.\n")
def is_exit_command(text: str) -> bool:
    return text.strip().lower() in EXIT_COMMANDS
# response = llm.invoke(
#     f"{secure_prompt}\n\nExplain OAuth2 in one paragraph"
# )
# print(response.content)

def get_text(response):
    if hasattr(response, "content"):
        return response.content
    return str(response)

def build_prompt(user_input: str) -> str:
    return f"""
{secure_prompt}

USER PROMPT:
{user_input}
"""

def detect_violation(response_text: str) -> bool:
    violation_markers = [
        "cannot comply",
        "not allowed",
        "policy",
        "violate",
        "refuse",
        "restricted",
        "forbidden"
    ]
    return any(marker in response_text.lower() for marker in violation_markers)

while True:
    try:
        user_input = input(">>> ").strip()

        if not user_input:
            continue

        if is_exit_command(user_input):
            print("\n Exiting!")
            sys.exit(0)

        prompt = build_prompt(user_input)

        response = llm.invoke(prompt)

        response_text = get_text(response)

        if detect_violation(response_text):
            print("\n  Prompt rejected due to policy violation.\n")
        else:
            print("\n Response:\n")
            print(response_text)
            print("\n" + "-" * 60)

    except KeyboardInterrupt:
        print("\n\nInterrupted. Exiting.")
        sys.exit(0)

    except Exception as e:
        print("\nERROR:")
        print(str(e))
        print("-" * 60)