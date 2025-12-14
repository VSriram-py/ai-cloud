from rag import load_rag_documents, build_or_load_vectorstore, retrieve_context
from utils import is_exit_command, is_prompt_leak_attempt, is_code_request

def main():
    try:
        documents = load_rag_documents()
    except Exception as e:
        print(f"Error loading documents: {e}")
        return

    if not documents:
        print("No documents found in RAG folder!")
        return

    try:
        vectorstore = build_or_load_vectorstore(documents)
    except ValueError as e:
        print(f"Error building vectorstore: {e}")
        return
    except Exception as e:
        # Catch Ollama connection or other embedding-related issues
        print(f"Error connecting to Ollama or building embeddings: {e}")
        print("Ensure Ollama is running and the 'nomic-embed-text:latest' model is pulled.")
        return

    print("\n--- RAG System Initialized ---")

    while True:
        query = input("Ask something (type 'exit' to quit): ").strip()

        if is_exit_command(query):
            break

        # OWASP AI Defense (Input Validation/Sanitization)
        if is_prompt_leak_attempt(query):
            # This aligns with Security Rule 1 & 2 of secure_prompt.txt
            print("\n[SECURITY REFUSAL] I cannot respond to requests that attempt to reveal my system instructions or internal policies.")
            continue
        
        if is_code_request(query):
            # This aligns with Security Rule 9 of secure_prompt.txt
            print("\n[POLICY REFUSAL] I cannot execute code. I can provide high-level explanations or non-operational examples.")
            continue

        if not query:
            continue

        print(f"\nProcessing query: '{query}'...")
        
        try:
            context = retrieve_context(query, vectorstore)
        except Exception as e:
            print(f"Error during context retrieval: {e}")
            continue

        print("\nRetrieved Context (Top-K Chunks):")
        if context:
            for i, c in enumerate(context):
                print(f"--- Chunk {i+1} ---")
                print(c[:500].replace("\n", " "), "...\n")
        else:
            print("No relevant context found.")

if __name__ == "__main__":
    main()