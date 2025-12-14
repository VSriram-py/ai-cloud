from dotenv import load_dotenv
from pathlib import Path
from langchain_ollama import ChatOllama
import sys
from utils import is_prompt_leak_attempt, detect_violation, handle_model_error
from rag import load_rag_documents, build_vectorstore, retrieve_context

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

# Load RAG data
RAG_FOLDER = Path(__file__).parent / "RAG"
documents = load_rag_documents(RAG_FOLDER)
vectorstore = build_vectorstore(documents)

# Helper functions
def get_text(response):
    if hasattr(response, "content"):
        return response.content
    return str(response)

def build_prompt(user_input: str, context: str = "") -> str:
    if context:
        return f"{secure_prompt}\n\nContext from knowledge base:\n{context}\n\nUSER PROMPT:\n{user_input}"
    return f"{secure_prompt}\n\nUSER PROMPT:\n{user_input}"

# Interactive loop
print("\nInteractive AI Console with RAG support")
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

        # RAG retrieval
        context, sources = retrieve_context(vectorstore, user_input)

        if not context:
            print("\nResponse:\n")
            print("I'm sorry, I do not have information on that topic in my knowledge base.\n")
            print("-" * 60)
            continue

        # Build prompt with retrieved context
        prompt = build_prompt(user_input, context)
        response = llm.invoke(prompt)
        response_text = get_text(response)

        if detect_violation(response_text):
            print("\nPrompt rejected due to policy violation.\n")
        else:
            print("\nResponse:\n")
            print(response_text)
            print("\nSources:")
            for src in sources:
                print(f"- {src}")
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
