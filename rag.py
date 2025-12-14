from pathlib import Path
import os
from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS 
from langchain_core.documents import Document 
import PyPDF2
# --- ADDED IMPORTS FOR LLM (Keep as requested) ---
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
# -------------------------------------------------

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
                # Ensure the source (file name) is saved in metadata
                documents.append(Document(page_content=text, metadata={"source": pdf_file.name}))
    return documents

# ONLY ONE DEFINITION FOR build_or_load_vectorstore (Using Ollama as requested)
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

# FIX 1: Returns Document objects to allow source name retrieval
def retrieve_context(query: str, vectorstore: FAISS, k: int = 5) -> list[Document]:
    """Retrieve top-k relevant Document objects for a query."""
    results = vectorstore.similarity_search(query, k=k)
    return results

# FIX 2: Added function for LLM generation and source formatting
def generate_rag_response(context_docs: List[Document], query: str) -> str:
    """
    Generates a final answer using the retrieved context and a Gemini LLM, 
    and appends the source file names to the output, without showing chunks.
    """
    if not os.getenv("GEMINI_API_KEY"):
        return "Error: GEMINI_API_KEY environment variable is not set. Cannot call Gemini LLM."

    # Using the user-requested model: gemini-3-pro-preview:latest
    llm = ChatGoogleGenerativeAI(model="gemini-3-pro-preview:latest") 

    # 1. Prepare context for the LLM
    context_text = "\n\n".join([doc.page_content for doc in context_docs])
    
    # 2. Extract unique source names
    sources = sorted(list(set([doc.metadata.get('source', 'Unknown File') for doc in context_docs])))
    source_list = "\n".join([f"* {source}" for source in sources])

    prompt_template = """
    You are a helpful and accurate RAG assistant. 
    Use ONLY the following retrieved context to answer the user's question. 
    The answer MUST be in a human-understandable format. 
    If the context does not contain the answer, state clearly and concisely: "I do not have the answer to that question in my documents."
    
    CONTEXT:
    {context}
    
    QUESTION:
    {question}
    
    ANSWER:
    """
    
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = prompt | llm
    
    print(f"Generating response with LLM ({llm.model} Cloud API call)...")

    try:
        response = chain.invoke({"context": context_text, "question": query})
        final_answer = response.content.strip()
    except Exception as e:
        final_answer = f"Error generating final response: {e}"
        
    # 3. Combine LLM response and source list
    return f"{final_answer}\n\n--- Source Documents Used ---\n{source_list}"