from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from pathlib import Path
import sys

load = load_dotenv(".env")

EXIT_COMMANDS = {"done", "exit", "quit", "q"}

FilePath = Path(__file__).parent / "secure_prompt.txt"
with open(FilePath, "r", encoding="utf-8") as f:
    secure_prompt = f.read().strip()

llm = ChatOllama(
    model="qwen3-vl:235b-cloud",
    #model="deepseek-v3.1:671b-cloud",
    #model="gemini-3-pro-preview",
    base_url="http://localhost:11434",
    temperature=0.5,
    #max_retries=3,
    max_tokens=250,
    system=secure_prompt
)

# response = llm.invoke(
#     f"{secure_prompt}\n\nExplain OAuth2 in one paragraph"
# )
# print(response.content)

print("\nInteractive AI Console")
print("Type your prompt. Type 'quit', 'exit', 'done', or 'q' to leave.\n")
def is_exit_command(text: str) -> bool:
    return text.strip().lower() in EXIT_COMMANDS

def get_text(response):
    if hasattr(response, "content"):
        return response.content
    return str(response)

def is_prompt_leak_attempt(text: str) -> bool:
    keywords = [
        "show me the prompt",
        "show me the prompts",
        "system prompt",
        "secure prompt",
        "internal instructions",
        "developer message",
        "hidden prompt",
        "system prompt",
        "secure prompt",
        "show prompt",
        "instructions",
        "developer message"
    ]
    return any(k in text.lower() for k in keywords)

def detect_violation(response_text: str) -> bool:
    refusal_phrases = [
        "i cannot show",
        "i can’t show",
        "cannot share",
        "internal instructions",
        "system prompt",
        "security boundaries",
        "security policy",
        "not allowed",
        "cannot comply",
        "i must refuse",
        "designed to provide helpful information while maintaining security",
    ]
    return any(phrase in response_text.lower() for phrase in refusal_phrases)

def build_prompt(user_input: str) -> str:
    return f"""
{secure_prompt}

USER PROMPT:
{user_input}
"""

def handle_model_error(error: Exception) -> bool:
    """
    Gracefully handle known Ollama / model errors.
    Returns True if handled.
    """
    msg = str(error).lower()

    if "403" in msg or "request limit" in msg or "premium model" in msg:
        print("\nModel access denied (403)")
        print("You have reached the request limit for this model.")
        print("Please wait, switch models, or check your subscription.\n")
        return True

    if "connection refused" in msg or "localhost:11434" in msg:
        print("\nOllama server is not reachable.")
        print("Make sure Ollama is running on http://localhost:11434\n")
        return True

    if "model" in msg and "not found" in msg:
        print("\nModel not found.")
        print("Make sure the model is pulled and the name is correct.\n")
        return True

    return False


while True:
    try:
        user_input = input(">>> ").strip()

        if not user_input:
            continue

        if is_exit_command(user_input):
            print("\nExiting!")
            sys.exit(0)

        # Pre-emptive protection
        if is_prompt_leak_attempt(user_input):
            print("\nPrompt rejected: access to system instructions is forbidden.\n")
            continue

        prompt = build_prompt(user_input)

        response = llm.invoke(prompt)
        response_text = get_text(response)

        # Post-response violation detection
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