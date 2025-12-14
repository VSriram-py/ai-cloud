from pathlib import Path
import sys

from dotenv import load_dotenv
from langchain_ollama import ChatOllama

from rag import load_rag_documents, build_or_load_vectorstore, retrieve_context


from utils import (
    is_exit_command,
    is_prompt_leak_attempt,
    detect_violation,
    handle_model_error,
)


load_dotenv()

BASE_DIR = Path(__file__).parent
#RAG_DIR = BASE_DIR / "RAG"
RAG_DIR = Path("RAG")

SECURE_PROMPT_FILE = BASE_DIR / "secure_prompt.txt"
secure_prompt = SECURE_PROMPT_FILE.read_text(encoding="utf-8").strip()

llm = ChatOllama(
    model="deepseek-v3.2:cloud",
    base_url="http://localhost:11434",
    temperature=0.5,
    max_tokens=300,
    system=secure_prompt,
)


documents = load_rag_documents(RAG_DIR)
vectorstore = build_or_load_vectorstore(documents)


if not documents:
    print("\nWARNING: No readable documents found in RAG folder.\n")

print("\nInteractive AI Console (RAG enabled)")
print("Type your prompt. Type 'quit', 'exit', 'done', or 'q' to leave.\n")


while True:
    try:
        user_input = input(">>> ").strip()

        if not user_input:
            continue

        if is_exit_command(user_input):
            print("\nExiting.")
            sys.exit(0)

        if is_prompt_leak_attempt(user_input):
            print("\nPrompt rejected: access to system instructions is forbidden.\n")
            continue

        context, sources = retrieve_context(vectorstore, user_input)

        if not context:
            print(
                "\nI can't help with that. "
                "My knowledge is limited to the provided documents.\n"
            )
            continue

        final_prompt = f"""
{secure_prompt}

CONTEXT (from documents):
{context}

USER QUESTION:
{user_input}
"""

        response = llm.invoke(final_prompt)
        response_text = response.content if hasattr(response, "content") else str(response)

        if detect_violation(response_text):
            print("\nResponse blocked due to policy violation.\n")
            continue

        print("\nResponse:\n")
        print(response_text)

        if sources:
            print("\nSources:")
            for s in sources:
                print(f"- {s}")

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
