# Silat Rulebook RAG System

This project is a complete Retrieval-Augmented Generation (RAG) system built to answer questions about the official Pencak Silat rulebook. It uses a local, open-source tech stack to parse a 700+ page PDF, embed its content into a vector database, and provide a user-friendly web interface for querying.

This was developed as a learning project to explore the end-to-end workflow of building a modern RAG application, from advanced document parsing to interactive UI deployment.

## Key Features

-   **Advanced PDF Parsing**: Intelligently processes a complex PDF, distinguishing between text-heavy pages and pages with visual content like tables and diagrams.
-   **Visual Content Handling**: Instead of using unreliable OCR, it generates descriptive "placeholders" for visual-heavy pages, guiding the user to the correct page in the PDF.
-   **Modern Embedding Strategy**: Utilizes a state-of-the-art Qwen embedding model (`Qwen/Qwen3-Embedding-0.6B`) with a large context window.
-   **Token-Based Chunking**: Leverages the model's large context window by splitting text into large, semantically rich chunks (4096 tokens).
-   **Local & Private**: The entire pipeline, from embedding to generation, runs locally using Ollama, ensuring data privacy.
-   **Interactive UI**: A simple and intuitive web interface built with Streamlit for asking questions and receiving answers.

## Tech Stack

-   **PDF Processing**: `PyMuPDF`
-   **Vector Database**: `ChromaDB`
-   **Orchestration Framework**: `LangChain`
-   **Embedding Model**: `Qwen/Qwen3-Embedding-0.6B` (via `sentence-transformers`)
-   **Generative LLM**: `Ollama` (with `llama3`)
-   **Frontend**: `Streamlit`

## Project Structure

```
.
├── app.py                  # The Streamlit frontend application
├── data/
│   ├── chroma_db/          # Persistent vector database
│   └── silat_rules_...pdf  # The source PDF document
├── docs/
│   ├── ...                 # Project planning and log files
├── main.py                 # Main ingestion script (run once)
├── rag_chain.py            # Core RAG query logic
├── README.md               # This file
├── requirements.txt        # Python dependencies
└── src/
    ├── config.py           # Central configuration for the project
    ├── content_analyzer.py # Logic for classifying page content
    ├── data_processor.py   # Handles text chunking, embedding, and storage
    ├── pdf_parser.py       # Extracts and cleans text from the PDF
    ├── pipeline_utils.py   # Helper functions for analysis and display
    └── text_processor.py   # Text cleaning and filtering utilities
```

## Setup and Installation

Follow these steps to get the project running on your local machine.

### Prerequisites

1.  **Python 3.10+**
2.  **Ollama**: Ensure you have [Ollama](https://ollama.com/) installed and running.
3.  **Local LLM**: Pull the generative model by running the following command in your terminal:
    ```bash
    ollama pull llama3
    ```

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd rag_system_v2
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Place the PDF**:
    -   Make sure you have the `silat_rules_and_regulations_version_7.pdf` file inside the `data/` directory.

## Usage

The project is divided into two main stages: a one-time data ingestion and the query application.

### 1. Ingestion Pipeline (Run this only once)

First, you need to process the PDF and populate the vector database.

```bash
python main.py
```

This script will:
-   Read and parse the PDF.
-   Clean and classify the content of each page.
-   Split the content into large, token-based chunks.
-   Generate embeddings using the Qwen model.
-   Store the embeddings in the `data/chroma_db` directory.

This process can take several minutes depending on your hardware, as it is downloading the embedding model and processing the entire document.

### 2. Run the Streamlit Application

Once the ingestion is complete, you can start the user interface.

```bash
streamlit run app.py
```

This will open a new tab in your browser with the application running. The first time you run it, it will take a moment to load the models into memory.

## Known Limitations & Future Improvements

As a learning project, the primary goal was implementation rather than achieving perfect output quality. The current system provides a solid foundation but has significant room for improvement.

-   **Answer Quality**: The quality of the generated answers is highly dependent on the retrieval quality and the capabilities of the local LLM. The responses are generally okay but may sometimes lack precision or provide irrelevant answers if the retrieved context is not perfect.

### 1. Data Ingestion and Preprocessing

The current process uses a straightforward token-based chunking strategy. This could be substantially improved:

-   **Semantic Chunking**: Instead of splitting by a fixed token count (`TOKEN_CHUNK_SIZE = 4096`), the ingestion script could be modified to split the document based on its logical structure (e.g., at the end of a "Section" or "Article"). This would create more semantically coherent chunks that are less likely to split a rule in the middle.
-   **Advanced Table/Figure Extraction**: The current system uses text placeholders for visual content. A more advanced approach would be to use a multimodal model or a library like `unstructured.io` to extract tables into a structured format (like Markdown) and generate detailed descriptions of diagrams, embedding this rich information directly.
-   **Metadata Enrichment**: The ingestion process could be enhanced to extract section and chapter titles as metadata for each chunk. This metadata could then be used to filter searches or provide more context to the LLM.

### 2. Retrieval and RAG Strategy

The retrieval process currently fetches the top 10 most similar documents (`k=10`). This can be made more sophisticated:

-   **Implement a Re-ranker**: A powerful technique is to retrieve a larger number of documents initially (e.g., `k=20`) and then use a more computationally expensive but accurate **cross-encoder model** (like `bge-reranker-large`) to re-rank these 20 documents and select the absolute best 3-5 to pass to the LLM. This significantly improves the signal-to-noise ratio of the context.
-   **Hybrid Search**: Combine the current semantic (dense) search with a traditional keyword-based (sparse) search like BM25. This helps with queries containing specific acronyms, codes, or proper nouns that semantic search might not perfectly capture.
-   **Query Transformation**: Use the LLM itself to improve the user's query before retrieval. Techniques like HyDE (Hypothetical Document Embeddings) involve generating a hypothetical answer to the user's question and using the embedding of that *answer* for the search, which can often be more effective than the query alone.

### 3. Models and Generation

-   **Embedding Model**: We are using `Qwen/Qwen3-Embedding-0.6B`, which is a strong, lightweight model. For higher accuracy at the cost of more resources, this could be upgraded to a larger model in the same family (e.g., `Qwen3-Embedding-4B`) or another top-performing model from the [MTEB Leaderboard](https://huggingface.co/spaces/mteb/leaderboard).
-   **Generative Model**: We are using the base `llama3` model. The final answer quality could be improved by using a larger, more capable model (e.g., `llama3:70b` if hardware permits) or by fine-tuning a model specifically on a Q&A dataset related to rules and regulations.

### 4. User Interface

-   **Source Linking**: The RAG chain is prompted to provide source page numbers, but the Streamlit UI does not yet parse these citations to provide clear, separate references or clickable links back to the PDF.

## License

This project is licensed under the MIT License.
