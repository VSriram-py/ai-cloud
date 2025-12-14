from pathlib import Path
import pickle

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings

# -----------------------
# CONFIG
# -----------------------
RAG_DIR = Path("RAG")
INDEX_DIR = Path(".rag_index")
INDEX_DIR.mkdir(exist_ok=True)

MAX_CHUNKS = 300
EMBED_MODEL = "nomic-embed-text"


# -----------------------
# LOAD DOCUMENTS (PDF)
# -----------------------
def load_rag_documents(rag_dir):
    documents = []

    if not rag_dir.exists():
        print("RAG folder not found.")
        return documents

    for pdf in rag_dir.glob("*.pdf"):
        loader = PyPDFLoader(str(pdf))
        pages = loader.load()

        for page in pages:
            page.metadata["source"] = pdf.name
            documents.append(page)

    return documents


# -----------------------
# BUILD VECTORSTORE
# -----------------------
def build_vectorstore(documents):
    if not documents:
        raise ValueError("No documents provided for vectorstore")

    if len(documents) > MAX_CHUNKS:
        print(f"Limiting chunks from {len(documents)} → {MAX_CHUNKS}")
        documents = documents[:MAX_CHUNKS]

    print(f"🔎 Building embeddings for {len(documents)} chunks...")

    embeddings = OllamaEmbeddings(
        model=EMBED_MODEL,
        base_url="http://localhost:11434",
    )

    vectorstore = FAISS.from_documents(documents, embeddings)
    return vectorstore


# -----------------------
# CACHE LOAD / SAVE
# -----------------------
def build_or_load_vectorstore(documents):
    index_file = INDEX_DIR / "faiss.pkl"

    if index_file.exists():
        print("Loading cached FAISS index...")
        with open(index_file, "rb") as f:
            return pickle.load(f)

    vectorstore = build_vectorstore(documents)

    with open(index_file, "wb") as f:
        pickle.dump(vectorstore, f)

    return vectorstore


# -----------------------
# RETRIEVAL
# -----------------------
def retrieve_context(vectorstore, query, k=3):
    results = vectorstore.similarity_search(query, k=k)

    if not results:
        return "", []

    context = "\n\n".join(d.page_content for d in results)
    sources = [d.metadata.get("source", "unknown") for d in results]

    return context, sources
