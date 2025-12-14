from typing import Set

EXIT_COMMANDS: Set[str] = {"done", "exit", "quit", "q"}

def is_exit_command(text: str) -> bool:
    return text.strip().lower() in EXIT_COMMANDS

def is_prompt_leak_attempt(text: str) -> bool:
    keywords = [
        "show me the prompt",
        "show me the prompts",
        "system prompt",
        "secure prompt",
        "internal instructions",
        "developer message",
        "hidden prompt",
        "show prompt",
    ]
    text = text.lower()
    return any(k in text for k in keywords)

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
    text = response_text.lower()
    return any(phrase in text for phrase in refusal_phrases)

def handle_model_error(error: Exception) -> bool:
    msg = str(error).lower()

    if "403" in msg or "request limit" in msg or "premium model" in msg:
        print("\nModel access denied (403). You have reached the request limit.\n")
        return True

    if "connection refused" in msg or "localhost:11434" in msg:
        print("\nOllama server is not reachable. Make sure Ollama is running.\n")
        return True

    if "model" in msg and "not found" in msg:
        print("\nModel not found. Check the model name.\n")
        return True

    return False
