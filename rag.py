from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter # Fix 1
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS # Fix 2
from langchain_core.documents import Document # FIX 3 (This is line 5)
import PyPDF2


RAG_DIR = Path(__file__).parent / "RAG"
INDEX_DIR = Path(__file__).parent / "vectorstore"
MAX_CHUNKS = 300

def load_rag_documents() -> list[Document]:
    """Load PDFs from RAG_DIR and split into documents."""
    documents = []
    if not RAG_DIR.exists():
        return []
    for pdf_file in RAG_DIR.glob("*.pdf"):
        with open(pdf_file, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            if text.strip():
                documents.append(Document(page_content=text, metadata={"source": pdf_file.name}))
    return documents

def build_or_load_vectorstore(documents: list[Document]) -> FAISS:
    """Build FAISS vectorstore using Ollama embeddings."""
    if not documents:
        raise ValueError("No documents to index!")

    # Limit chunks to avoid context length errors
    if len(documents) > MAX_CHUNKS:
        documents = documents[:MAX_CHUNKS]

    # Split documents into smaller chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_documents(documents)

    # Build embeddings
    embeddings = OllamaEmbeddings(model="nomic-embed-text:latest")
    vectorstore = FAISS.from_documents(chunks, embeddings)
    return vectorstore

def retrieve_context(query: str, vectorstore: FAISS, k: int = 5) -> list[str]:
    """Retrieve top-k relevant chunks for a query."""
    results = vectorstore.similarity_search(query, k=k)
    return [r.page_content for r in results]