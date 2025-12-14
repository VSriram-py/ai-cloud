from rag import load_rag_documents, build_or_load_vectorstore, retrieve_context

def main():
    documents = load_rag_documents()
    if not documents:
        print("No documents found in RAG folder!")
        return

    vectorstore = build_or_load_vectorstore(documents)

    while True:
        query = input("Ask something (type 'exit' to quit): ").strip()
        if query.lower() in {"exit", "quit", "done"}:
            break

        context = retrieve_context(query, vectorstore)
        print("\nRetrieved Context:")
        for c in context:
            print("-", c[:300].replace("\n", " "), "...\n")

if __name__ == "__main__":
    main()
