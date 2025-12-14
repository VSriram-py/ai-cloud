from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
import PyPDF2

# Use a relative path from the current file's directory
BASE_DIR = Path(__file__).parent 
RAG_DIR = BASE_DIR / "RAG"
INDEX_DIR = BASE_DIR / "vectorstore"
MAX_CHUNKS = 300

def load_rag_documents() -> list[Document]:
    """Load PDFs from RAG_DIR and split into documents."""
    documents = []
    if not RAG_DIR.exists():
        print(f"Warning: RAG directory not found at {RAG_DIR}. Returning empty document list.")
        return []
        
    print(f"Searching for PDFs in {RAG_DIR}...")
    for pdf_file in RAG_DIR.glob("*.pdf"):
        try:
            with open(pdf_file, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() or ""
                if text.strip():
                    documents.append(Document(page_content=text, metadata={"source": pdf_file.name}))
        except Exception as e:
            print(f"Error processing PDF {pdf_file.name}: {e}")
            
    print(f"Found {len(documents)} document(s).")
    return documents

def build_or_load_vectorstore(documents: list[Document]) -> FAISS:
    """Build FAISS vectorstore using Ollama embeddings."""
    if not documents:
        # This check is also in ragtest.py, but remains a good practice here
        raise ValueError("No documents were loaded to index!")

    # Apply chunk limit
    if len(documents) > MAX_CHUNKS:
        print(f"Warning: Limiting documents from {len(documents)} to {MAX_CHUNKS} to avoid context issues.")
        documents = documents[:MAX_CHUNKS]

    # Split documents into smaller chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_documents(documents)
    print(f"Documents split into {len(chunks)} chunks.")

    # Build embeddings
    # NOTE: This line may raise a connection error if Ollama is not running
    print("Building embeddings using Ollama...")
    embeddings = OllamaEmbeddings(model="nomic-embed-text:latest")
    vectorstore = FAISS.from_documents(chunks, embeddings)
    print("Vectorstore built successfully.")
    return vectorstore

def retrieve_context(query: str, vectorstore: FAISS, k: int = 5) -> list[str]:
    """Retrieve top-k relevant chunks for a query."""
    print(f"Retrieving top {k} context chunk(s)...")
    results = vectorstore.similarity_search(query, k=k)
    return [r.page_content for r in results]