from typing import Set

EXIT_COMMANDS: Set[str] = {"done", "exit", "quit", "q"}

def is_exit_command(text: str) -> bool:
    return text.strip().lower() in EXIT_COMMANDS

def is_code_request(text: str) -> bool:
    """
    Checks for keywords indicating a request for executable code,
    which violates the system's execution safety rules. [cite: 8, 9]
    """
    keywords = [
        # Direct requests for code
        "write a program",
        "write code",
        "generate code",
        "show me the code",
        "give me a function",
        "implementation",
        # Language/context keywords
        "python",
        "script",
        "bash",
        "shell",
        "javascript",
        "java",
        "c++",
        "c#",
        "executable",
        # Request for examples/templates
        "example code",
        "code snippet",
        "template",
        "payload",
    ]
    return any(k in text.lower() for k in keywords)

def is_prompt_leak_attempt(text: str) -> bool:
    """
    Checks for keywords indicating an attempt to reveal system prompts,
    internal instructions, or hidden policies, which violates security rules. [cite: 1]
    """
    keywords = [
        # Direct prompt/instruction leakage attempts [cite: 1]
        "show me the prompt",
        "system prompt",
        "internal instructions",
        "hidden prompt",
        "developer instructions",
        "system rules",
        "system config",
        "embedding",
        "chain-of-thought",
        "hidden policies",
        # Commands to manipulate prompt/context [cite: 2]
        "ignore previous rules",
        "override system",
        "jailbreak",
        "stop pretending",
        "confidential instructions",
        "private data",
    ]
    return any(k in text.lower() for k in keywords)