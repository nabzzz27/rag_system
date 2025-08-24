import re
from typing import Dict, Any
from src.config import BOILERPLATE_PATTERNS

def clean_text(text: str) -> str:
    """Removes boilerplate patterns from the extracted text."""
    cleaned = text
    for pattern in BOILERPLATE_PATTERNS:
        cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE | re.MULTILINE)
    
    # Remove excessive whitespace and normalize
    cleaned = re.sub(r'\n\s*\n', '\n\n', cleaned)  # Normalize multiple newlines
    cleaned = re.sub(r'[ \t]+', ' ', cleaned)      # Normalize spaces and tabs
    cleaned = cleaned.strip()
    
    return cleaned

def filter_page(page_number: int, text_content: str) -> bool:
    """Determines if a page should be included based on content and page number."""
    from src.config import PAGES_TO_SKIP
    
    # Check if page is in the explicit skip list
    if page_number in PAGES_TO_SKIP:
        return False  # Skip this page
    
    return True  # Include this page
