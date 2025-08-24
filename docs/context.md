# Project Plan: Silat Rulebook RAG System

## 1. Project Scoping
- **Problem Statement:** Athletes and the general public often struggle to quickly find and understand specific rules, and refer to relevant visual aids, within a large, 700-page Silat rulebook PDF. The current manual search process is time-consuming and inefficient, hindering rapid clarification and understanding of regulations.
- **Objectives:**
    - To develop an intuitive, accessible Retrieval-Augmented Generation (RAG) system that provides accurate and non-hallucinated answers to natural language queries about the Silat rulebook.
    - To enhance responses by providing specific page numbers and direct, clickable links to the relevant sections/pages within the original PDF for easy reference, particularly for pages containing important visual information.
    - To ensure the system delivers responses with reasonable speed, providing a practical tool for quick lookups.
    - To design the system with modularity and robustness to allow for potential future expansion to other documents or updated rulebook versions.
- **Target Audience:** Silat athletes, practitioners, judges, instructors, and the general public seeking quick and accurate rule clarifications and contextual reference to visual information.
- **Key Features (MVP):**
    - User-friendly web interface (Streamlit) for submitting natural language queries.
    - AI-generated textual responses based on information retrieved from the Silat rulebook PDF.
    - Display of specific page numbers (e.g., "Page 123") from the PDF that are most relevant to the generated response.
    - Provision of clickable, direct links (e.g., `file.pdf#page=123`) to those relevant pages within the original PDF.
    - Ability to process and retrieve information from the entire 700-page, text-searchable PDF, including identifying pages where relevant images are present for user reference.
- **Constraints & Assumptions:**
    - **Time:** Project completion is targeted within a few days, suitable for a solo developer.
    - **Resources:** Solutions will prioritize free/freemium tools and local execution where feasible, minimizing external service costs.
    - **PDF Structure:** The Silat rulebook PDF contains mixed content: text-searchable pages and image-based pages (tables, forms, diagrams). Page numbering is consistent and reliable.
    - **Image Handling:** Complex visual content (tables, forms) will be handled through intelligent placeholders and user guidance to original PDF pages, rather than OCR extraction. Direct rendering of images within the UI is out of scope for the MVP.
    - **Accuracy & Hallucination:** It is critical that the system does not hallucinate or provide incorrect information; accuracy is paramount.
    - **Performance:** Response times should be reasonable (e.g., a few seconds) rather than instantaneous, balancing speed with accuracy and local resource constraints.
    - **Scalability:** The initial scope is limited to this single PDF. Modularity for future expansion is a design consideration but not the primary driver for immediate architectural complexity.

## 2. Tech Stack Recommendation
- **Preferred Stack:**
    - **PDF Parsing:** `PyMuPDF (fitz)` - Selected for its speed, robustness, and ability to extract text, page numbers, and identify image locations/pages from complex PDFs. This will be crucial for associating text with source pages for linking.
    - **Orchestration/RAG Framework:** `LangChain` - The industry-standard framework for building LLM applications, offering comprehensive abstractions for RAG pipeline components (loaders, splitters, retrievers, LLMs). Simplifies development and promotes modularity.
    - **Text Splitting:** `LangChain.text_splitter.RecursiveCharacterTextSplitter` - A versatile text splitter that intelligently breaks down documents while attempting to preserve semantic context, crucial for effective retrieval from a large rulebook.
    - **Embedding Model:** `sentence-transformers/all-MiniLM-L6-v2` (via `HuggingFaceEmbeddings` in LangChain) - A compact, efficient, and entirely free embedding model. It runs locally, eliminating API costs while providing strong semantic similarity performance for retrieval.
    - **Vector Database:** `ChromaDB` (local, persistent) - A lightweight, open-source vector store designed for local development and research. It's easy to set up, supports persistence (storing embeddings on disk), and integrates seamlessly with LangChain.
    - **Language Model (LLM):** `Ollama` with `Llama 3 8B` or `Mistral 7B` - Ollama provides an easy way to download and run various open-source LLMs locally, ensuring privacy and eliminating API costs. `Llama 3 8B` or `Mistral 7B` offer a good balance of quality and performance for local inference.
    - **Frontend UI:** `Streamlit` - Chosen for its ability to rapidly build interactive web applications purely in Python. It's ideal for prototyping a user-friendly interface to demonstrate the RAG system's capabilities, allowing for easy input and structured display of results and links.

- **Alternatives & Trade-offs:**
    - **PDF Parsing:** *Alternative:* `unstructured.io`. *Trade-off:* While more feature-rich for complex document understanding, it introduces additional dependencies and complexity that may exceed the "few days" project scope. `PyMuPDF` provides sufficient capability for MVP needs.
    - **Embedding Model:** *Alternative:* OpenAI Embeddings (`text-embedding-ada-002`). *Trade-off:* Offers potentially higher embedding quality and convenience via API, but incurs usage costs per token. `all-MiniLM-L6-v2` is free and adequate for this scale.
    - **Vector Database:** *Alternative:* `FAISS` (Facebook AI Similarity Search). *Trade-off:* Extremely fast for similarity search, but primarily an in-memory indexing library rather than a full-fledged database with built-in persistence and robust client capabilities like `ChromaDB`.
    - **Language Model (LLM):** *Alternative:* OpenAI GPT models (`gpt-3.5-turbo`, `gpt-4o`). *Trade-off:* State-of-the-art performance and widely adopted, but are proprietary, incur significant costs for high usage, and require sending data to an external API. Local LLMs via `Ollama` offer cost control and data privacy.
    - **Frontend UI:** *Alternative:* `Gradio`. *Trade-off:* Also excellent for quick ML demos, but `Streamlit` often provides more flexibility in layout and component design, allowing for a slightly more polished user experience for displaying formatted text and clickable links.

## 3. System Architecture
- **High-Level Breakdown:**
  - **Frontend (Streamlit UI):** The user-facing component that handles query input, displays the generated answers, and presents the relevant page numbers with clickable links to the PDF. It orchestrates user interaction with the backend logic.
  - **Backend (Python Script/LangChain Application):** The core logic module that encapsulates the RAG pipeline. It manages the loading, processing, indexing, retrieval, and LLM interaction. This includes:
      - **Document Ingestion:** One-time (or on update) process to parse the PDF, chunk its content, embed chunks, and store them in the vector database.
      - **Query Processing:** On user query, it embeds the query, retrieves relevant text chunks from the vector database, formats a prompt with context, and interacts with the LLM.
      - **Response Generation:** Receives the LLM's output and extracts/formats the final answer, including identifying all unique page numbers from the retrieved chunks to generate direct PDF links.
  - **Database (ChromaDB):** A local, file-based vector store that persists the embeddings of the PDF's text chunks. Each embedding will be stored with rich metadata, crucially including the `page_number` from which the text originated and a flag indicating if the page also contains images.
  - **APIs/Integrations:**
      - `Ollama` API: Local HTTP interface to interact with the downloaded open-source LLM for inference.
      - `PyMuPDF` Library: Used by the Backend for efficient PDF text and metadata extraction.
      - `LangChain` Library: Acts as the primary framework for building and connecting all RAG components.
      - `Sentence Transformers`: Handles the loading and execution of the `all-MiniLM-L6-v2` embedding model.

- **Data Flow / Architecture Sketch (Query Pipeline Detail):**

| Flow Step | Component             | Key Action(s)                                                                       |
| :-------- | :-------------------- | :---------------------------------------------------------------------------------- |
| 1. Input  | User                  | Submits a natural language query via the web interface.                             |
| 2. Frontend Request | Streamlit UI          | Receives user query and sends it to the LangChain application (Backend).            |
| 3. Backend (Retrieval) | LangChain App         | Embeds the user query. Performs a similarity search in ChromaDB to retrieve the most relevant text chunks from the PDF.                                  |
| 4. Backend (Contextualization) | LangChain App         | Constructs a detailed prompt for the LLM, incorporating the original query and the retrieved relevant text chunks as context. |
| 5. LLM Inference | Ollama (Local LLM)    | Receives the prompt from LangChain App. Generates a coherent and accurate response based on the provided context. |
| 6. Backend (Post-processing) | LangChain App         | Receives the LLM's generated response. Extracts unique page numbers from the metadata of the retrieved chunks that contributed to the answer. Formats the final response including the text and clickable PDF links. |
| 7. Output | Streamlit UI / User   | Displays the generated response, the relevant page numbers, and direct, clickable links to those pages in the PDF for the user. |


## 4. Risks & Blockers
-   **Visual Content Handling:** Complex tables and forms are best viewed in their original PDF format rather than extracted as text. The system addresses this through intelligent content type detection and meaningful placeholder text that guides users to the appropriate PDF pages for visual content.
-   **Local LLM Performance and Resource Consumption:** Running a 7B or 8B parameter LLM via Ollama locally necessitates substantial RAM (16GB+ minimum, 32GB+ recommended) and potentially a dedicated GPU for acceptable inference speeds. If the development machine's resources are limited, response times could be slow, or the model might fail to load. This needs to be tested early.
-   **Optimal Chunking Strategy:** Determining the ideal `chunk_size` and `chunk_overlap` for the `RecursiveCharacterTextSplitter` is critical for retrieval quality. Incorrect chunking can lead to irrelevant context or fragmented information, increasing the risk of hallucination or incomplete answers. This will require iterative experimentation and fine-tuning.
-   **Initial Indexing Time:** Processing and embedding a 700-page PDF, even with optimized libraries, will take a significant amount of time during the initial ingestion phase. This is a one-time setup cost but needs to be factored into the project timeline.
-   **Direct PDF Link Compatibility:** While standard `#page=X` links are widely supported, their exact behavior (e.g., opening a new tab, requiring a local PDF viewer) can vary across browsers and user system configurations. This should be tested.