from typing import Set

EXIT_COMMANDS: Set[str] = {"done", "exit", "quit", "q"}

def is_exit_command(text: str) -> bool:
    return text.strip().lower() in EXIT_COMMANDS

def is_code_request(text: str) -> bool:
    keywords = [
        "write a program",
        "write code",
        "python",
        "script",
        "example code",
        "implementation",
    ]
    return any(k in text.lower() for k in keywords)

def is_prompt_leak_attempt(text: str) -> bool:
    keywords = [
        "show me the prompt",
        "system prompt",
        "internal instructions",
        "hidden prompt",
    ]
    return any(k in text.lower() for k in keywords)
