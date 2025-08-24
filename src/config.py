# PDF Processing Configuration
PDF_PATH = "data/silat_rules_and_regulations_version_7.pdf"
CHROMA_DB_DIR = "data/chroma_db"
CHROMA_COLLECTION_NAME = "silat_rules"

# Text Cleaning Parameters
# Use raw strings (r"...") for regex patterns
BOILERPLATE_PATTERNS = [
    r"Copyright © \d{2} October \d{4} Version \d+ by International Pencak Silat Federation \(PERSILAT\)\. All rights reserved\.",
    r"No part of this material/publication may be reproduced or published in any manner without the consent in writing\.",
    # Add more patterns as we discover them
    r"^\s*Table of Contents\s*$",  # Table of contents headers
    r"^\s*Contents\s*$",  # Simple contents headers
]

# Page Filtering Parameters
# Pages to explicitly skip (1-indexed page numbers)
PAGES_TO_SKIP = list(range(1, 15))  # Cover page, title page, table of contents - adjust based on inspection
# Removed MIN_TEXT_LENGTH_THRESHOLD - we want to keep image-based pages

# OCR Configuration
OCR_ENABLED = True
OCR_MIN_TEXT_THRESHOLD = 50  # Only attempt OCR if PDF text layer has less than this many characters
OCR_CONFIDENCE_THRESHOLD = 30  # Minimum confidence for OCR text (0-100)
# Tesseract path for Windows (adjust if installed elsewhere)
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# --- Embedding Model and Chunking Strategy ---
# Using a powerful Qwen embedding model with a large context window.
# This allows for a token-based chunking strategy for better semantic context.
EMBEDDING_MODEL_NAME = "Qwen/Qwen3-Embedding-0.6B"

# We now use token-based chunking to be more precise with the model's context window.
# A larger chunk size is chosen to leverage the model's 32k token capacity.
TOKEN_CHUNK_SIZE = 4096
TOKEN_CHUNK_OVERLAP = 512

# The old character-based chunking parameters are no longer used.
# CHUNK_SIZE = 1000
# CHUNK_OVERLAP = 200

# --- RAG Pipeline Configuration ---
# The local LLM to use for generating answers.
# Make sure you have pulled this model with "ollama pull <model_name>"
LLM_MODEL_NAME = "llama3"
