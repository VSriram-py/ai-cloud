from typing import Any

PROMPT_LEAK_KEYWORDS = frozenset([
    "show me the prompt",
    "show me the prompts",
    "system prompt",
    "secure prompt",
    "internal instructions",
    "developer message",
    "hidden prompt",
])

def is_prompt_leak_attempt(text: str) -> bool:
    """
    Check if user input attempts to access system or secure prompts.
    Time Complexity: O(n * k), where n = len(text), k = number of keywords (small constant)
    Memory Complexity: O(1) extra memory
    """
    if not text:
        return False
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in PROMPT_LEAK_KEYWORDS)

VIOLATION_PHRASES = frozenset([
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
])

def detect_violation(response_text: str) -> bool:
    """
    Detect if model response violates internal policy.
    Time Complexity: O(m * p), m = len(response_text), p = # of phrases (small constant)
    Memory Complexity: O(1) extra memory
    """
    if not response_text:
        return False
    text_lower = response_text.lower()
    return any(phrase in text_lower for phrase in VIOLATION_PHRASES)


def handle_model_error(error: Exception) -> bool:
    """
    Gracefully handle known Ollama / model errors.
    Returns True if handled.
    Time Complexity: O(e), e = length of error string
    Memory Complexity: O(1)
    """
    if error is None:
        return False

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
