from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.docstore.document import Document
from pathlib import Path

def load_rag_documents(rag_folder: Path):
    """Load all text files from RAG folder as Documents."""
    documents = []
    for file_path in rag_folder.glob("**/*.txt"):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
                documents.append(Document(page_content=text, metadata={"source": str(file_path)}))
        except Exception:
            continue
    return documents

def build_vectorstore(documents):
    """Split documents and create a FAISS vectorstore."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = text_splitter.split_documents(documents)
    embeddings = OpenAIEmbeddings()  # Replace with other embeddings if needed
    return FAISS.from_documents(docs, embeddings)

def retrieve_context(vectorstore, query: str, top_k: int = 3):
    """Retrieve relevant context and source files."""
    results = vectorstore.similarity_search(query, k=top_k)
    if not results:
        return "", []

    combined_text = "\n".join([doc.page_content for doc in results])
    sources = [doc.metadata.get("source", "unknown") for doc in results]
    return combined_text, sources
