import torch
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.docstore.document import Document
from langchain.text_splitter import TokenTextSplitter
from typing import List, Dict, Any

from src.config import (CHROMA_DB_DIR, CHROMA_COLLECTION_NAME, 
                       EMBEDDING_MODEL_NAME, TOKEN_CHUNK_SIZE, TOKEN_CHUNK_OVERLAP)

def get_embeddings_model() -> HuggingFaceEmbeddings:
    """
    Initializes the HuggingFace embeddings model with specific configurations
    for advanced models like Qwen.
    """
    # Automatically use GPU if available, otherwise CPU
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Using device: {device}")

    # Models like Qwen require trusting remote code to run their custom architecture.
    # Normalizing embeddings is a best practice for retrieval tasks.
    model_kwargs = {
        'device': device,
        'trust_remote_code': True 
    }
    encode_kwargs = {'normalize_embeddings': True}
    
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )

def get_token_text_splitter() -> TokenTextSplitter:
    """
    Initializes a token-based text splitter, which is more precise for models
    with large context windows.
    """
    return TokenTextSplitter(
        # The model_name parameter is not directly supported in all versions,
        # but the splitter will use the default tokenizer for tiktoken if not specified,
        # which is a reasonable default. For more precise token counting,
        # one might need to load the tokenizer explicitly.
        chunk_size=TOKEN_CHUNK_SIZE,
        chunk_overlap=TOKEN_CHUNK_OVERLAP
    )

def prepare_documents_for_chroma(extracted_pages_data: List[Dict[str, Any]]) -> List[Document]:
    """Converts raw extracted page data into LangChain Document objects."""
    return [
        Document(
            page_content=page_data['text'],
            metadata={k: v for k, v in page_data.items() if k != 'text'}
        ) for page_data in extracted_pages_data
    ]

def process_and_store_data(extracted_pages_data: List[Dict[str, Any]]):
    """Orchestrates chunking, embedding, and storage of documents in ChromaDB."""
    print("Initializing components for data processing...")
    embedding_model = get_embeddings_model()
    text_splitter = get_token_text_splitter()

    print(f"Preparing {len(extracted_pages_data)} pages into LangChain Documents...")
    initial_docs = prepare_documents_for_chroma(extracted_pages_data)

    print(f"Splitting {len(initial_docs)} documents into token-based chunks...")
    chunks = text_splitter.split_documents(initial_docs)
    print(f"  Split into {len(chunks)} chunks.")
    
    print("Initializing ChromaDB for vector storage...")
    vector_store = Chroma(
        collection_name=CHROMA_COLLECTION_NAME,
        persist_directory=CHROMA_DB_DIR,
        embedding_function=embedding_model
    )
    
    print(f"Adding {len(chunks)} chunks to ChromaDB. This may take some time...")
    vector_store.add_documents(chunks)
    
    print("Persisting the database to disk...")
    vector_store.persist()
    
    print(f"Successfully added {len(chunks)} chunks to ChromaDB.")
