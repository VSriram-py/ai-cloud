from pathlib import Path
#import pickle

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings

# -----------------------
# CONFIG
# -----------------------
RAG_DIR = Path("RAG")
INDEX_DIR = Path(".rag_index")
INDEX_DIR.mkdir(exist_ok=True)

EMBED_MODEL = "nomic-embed-text"

CHUNK_SIZE = 500        # SAFE for Ollama
CHUNK_OVERLAP = 50
MAX_CHUNKS = 300        # HARD safety cap


# -----------------------
# LOAD + CHUNK PDFS
# -----------------------
def load_rag_documents(rag_dir: Path):
    documents = []

    if not rag_dir.exists():
        print("RAG folder not found.")
        return documents

    for pdf in rag_dir.glob("*.pdf"):
        loader = PyPDFLoader(str(pdf))
        pages = loader.load()

        for page in pages:
            text = page.page_content
            source = pdf.name

            # Manual lightweight chunking (NO langchain splitter)
            start = 0
            while start < len(text):
                chunk = text[start : start + CHUNK_SIZE]
                documents.append(
                    {
                        "text": chunk,
                        "source": source,
                    }
                )
                start += CHUNK_SIZE - CHUNK_OVERLAP

    if len(documents) > MAX_CHUNKS:
        print(f"Limiting chunks from {len(documents)} → {MAX_CHUNKS}")
        documents = documents[:MAX_CHUNKS]

    return documents


# -----------------------
# BUILD VECTORSTORE
# -----------------------
def build_vectorstore(documents):
    if not documents:
        raise ValueError("No documents to embed")

    print(f"Building embeddings for {len(documents)} chunks...")

    texts = [d["text"] for d in documents]
    metadatas = [{"source": d["source"]} for d in documents]

    embeddings = OllamaEmbeddings(
        model=EMBED_MODEL,
        base_url="http://localhost:11434",
    )

    return FAISS.from_texts(texts, embeddings, metadatas=metadatas)


# -----------------------
# CACHE VECTORSTORE
# -----------------------
def build_or_load_vectorstore(documents):
    index_path = INDEX_DIR / "faiss_index"

    embeddings = OllamaEmbeddings(
        model=EMBED_MODEL,
        base_url="http://localhost:11434",
    )

    if index_path.exists():
        print("📦 Loading cached FAISS index...")
        return FAISS.load_local(
            str(index_path),
            embeddings,
            allow_dangerous_deserialization=True,
        )

    vectorstore = build_vectorstore(documents)

    print("💾 Saving FAISS index to disk...")
    vectorstore.save_local(str(index_path))

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
