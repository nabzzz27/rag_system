from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from typing import Dict, Any

from src.data_processor import get_embeddings_model
from src.config import CHROMA_DB_DIR, CHROMA_COLLECTION_NAME, LLM_MODEL_NAME

def get_retriever():
    """
    Creates and returns a retriever from the persistent ChromaDB vector store.
    """
    print("Loading embedding model for retriever...")
    embedding_function = get_embeddings_model()
    
    print(f"Loading ChromaDB from: {CHROMA_DB_DIR}")
    vector_store = Chroma(
        collection_name=CHROMA_COLLECTION_NAME,
        persist_directory=CHROMA_DB_DIR,
        embedding_function=embedding_function
    )
    
    print(f"ChromaDB loaded. Number of documents: {vector_store._collection.count()}")
    return vector_store.as_retriever(search_kwargs={"k": 10})

def format_docs(docs: list) -> str:
    """
    Formats the retrieved documents into a single string for the prompt.
    Includes page number and a note for visual content.
    """
    formatted_docs = []
    unique_pages = set()
    for doc in docs:
        metadata = doc.metadata
        page_num = metadata.get('page_number', 'N/A')
        
        # Avoid duplicating the same page content if multiple chunks are retrieved
        if page_num in unique_pages:
            continue
        unique_pages.add(page_num)

        content = doc.page_content
        header = f"--- START OF DOCUMENT FROM PAGE {page_num} ---"
        footer = f"--- END OF DOCUMENT FROM PAGE {page_num} ---\n"
        
        if metadata.get('is_visual_reference', False):
            content += "\n\n[NOTE: This is a placeholder for a page with significant visual content like tables or diagrams. Refer to the original PDF page for full context.]"

        formatted_docs.append(f"{header}\n{content}\n{footer}")
        
    return "\n".join(formatted_docs)

def create_rag_chain():
    """
    Creates the complete RAG chain for processing queries.
    """
    retriever = get_retriever()
    llm = Ollama(model=LLM_MODEL_NAME)
    
    prompt_template = """
    You are an expert assistant for the Pencak Silat rulebook. Your task is to provide accurate, clear, and concise answers based ONLY on the provided context. Do not use any outside knowledge.

    CONTEXT:
    {context}

    QUESTION:
    {question}

    INSTRUCTIONS:
    1.  Answer the question using only the information from the context above.
    2.  If the context does not contain the answer, state clearly "The provided context does not contain enough information to answer this question."
    3.  Cite the page number(s) from which you derived your answer (e.g., "Source: Page 123"). If the information comes from multiple pages, cite them all.
    4.  If the context includes a note about visual content (tables, diagrams), explicitly advise the user to refer to that page in the PDF for the visual information.
    5.  Do not make up information or hallucinate.
    """
    
    prompt = ChatPromptTemplate.from_template(prompt_template)
    
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain

def query_rag_chain(query: str, chain):
    """Helper function to test the RAG chain."""
    print("\n" + "="*50)
    print(f"Query: {query}")
    print("="*50)
    response = chain.invoke(query)
    print(f"Response:\n{response}")
    print("="*50)

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        test_query = " ".join(sys.argv[1:])
        print("Creating RAG chain for testing...")
        test_chain = create_rag_chain()
        query_rag_chain(test_query, test_chain)
    else:
        print("Please provide a query to test the RAG chain.")
        print('Example: python src/rag_chain.py "What are the competition categories?"')
