from rag import load_rag_documents, build_or_load_vectorstore, retrieve_context, generate_rag_response # FIX 3: Import the new function

def main():
    documents = load_rag_documents()
    if not documents:
        print("No documents found in RAG folder!")
        return

    vectorstore = build_or_load_vectorstore(documents)
    
    print("\n--- RAG System Initialized (Using Gemini Cloud API) ---")
    
    while True:
        query = input("Ask something (type 'exit' to quit): ").strip()
        if query.lower() in {"exit", "quit", "done"}:
            break

        try:
            # FIX 4: retrieve_context now returns Document objects
            context_documents = retrieve_context(query, vectorstore)
            
            # FIX 5: Call the new function to generate the answer and sources
            final_response = generate_rag_response(context_documents, query)
            print(final_response)

        except Exception as e:
            # Catch errors outside of the LLM call (e.g., retrieval)
            print(f"Error during RAG process: {e}")
            
        # The manual context printing loop is now REMOVED as requested.


if __name__ == "__main__":
    main()