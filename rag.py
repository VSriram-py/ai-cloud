from pathlib import Path
from typing import List, Tuple
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings


def load_rag_documents(rag_dir: Path):
    documents = []

    if not rag_dir.exists():
        return documents

    for path in rag_dir.rglob("*"):
        try:
            text = ""

            if path.suffix.lower() == ".txt":
                text = path.read_text(encoding="utf-8").strip()

            elif path.suffix.lower() == ".pdf":
                reader = PdfReader(path)
                text = "\n".join(
                    page.extract_text() or "" for page in reader.pages
                ).strip()

            if text:
                documents.append(
                    Document(
                        page_content=text,
                        metadata={"source": path.name}
                    )
                )

        except Exception:
            continue

    return documents



def build_vectorstore(documents: List[Document]) -> FAISS | None:
    if not documents:
        return None  # 🔴 critical guard

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=40
    )

    chunks = splitter.split_documents(documents)

    if not chunks:
        return None  # 🔴 second guard

    embeddings = OllamaEmbeddings(
        model="nomic-embed-text",
        base_url="http://localhost:11434"
    )

    return FAISS.from_documents(chunks, embeddings)


def retrieve_context(
    vectorstore: FAISS | None,
    query: str,
    k: int = 3
) -> Tuple[str, List[str]]:

    if vectorstore is None:
        return "", []

    results = vectorstore.similarity_search(query, k=k)

    if not results:
        return "", []

    context = "\n".join(r.page_content for r in results)
    sources = list({r.metadata.get("source", "unknown") for r in results})

    return context, sources
