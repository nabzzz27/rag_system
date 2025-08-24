import fitz  # PyMuPDF
import re
from typing import List, Dict, Any
from PIL import Image
import pytesseract
import io
import os
from src.config import (BOILERPLATE_PATTERNS, PAGES_TO_SKIP, OCR_ENABLED, 
                       OCR_MIN_TEXT_THRESHOLD, OCR_CONFIDENCE_THRESHOLD, TESSERACT_PATH)

# Configure pytesseract to point to your Tesseract installation
if OCR_ENABLED and os.path.exists(TESSERACT_PATH):
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

import fitz
from typing import List, Dict, Any
from src.text_processor import clean_text, filter_page
from src.content_analyzer import analyze_page_content, create_visual_content_placeholder

def extract_text_with_metadata(pdf_path: str) -> List[Dict[str, Any]]:
    """
    Extracts text and metadata from PDF pages with smart handling of visual content.
    """
    documents = []
    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    skipped_pages = []
    visual_heavy_pages = []
    
    print(f"Processing {total_pages} pages with smart visual content handling...")
    
    for page_num, page in enumerate(doc):
        page_number_1_indexed = page_num + 1
        
        if page_number_1_indexed % 50 == 0:  # Progress indicator
            print(f"  Processed {page_number_1_indexed}/{total_pages} pages...")
        
        # 1. Get text from PDF layer
        text_from_pdf_layer = page.get_text()
        
        # 2. Analyze page content
        content_analysis = analyze_page_content(page, text_from_pdf_layer)
        
        # 3. Clean the text
        cleaned_text = clean_text(text_from_pdf_layer)
        
        # 4. Apply filtering
        if not filter_page(page_number_1_indexed, cleaned_text):
            skipped_pages.append(page_number_1_indexed)
            continue
        
        # 5. Handle different content types
        final_text = ""
        
        if content_analysis["content_type"] == "visual_heavy":
            # Create a meaningful placeholder instead of OCR gibberish
            final_text = create_visual_content_placeholder(page_number_1_indexed, content_analysis)
            visual_heavy_pages.append(page_number_1_indexed)
        else:
            # Use the cleaned PDF text
            final_text = cleaned_text
        
        # 6. Store the page data
        if final_text.strip():
            documents.append({
                "text": final_text,
                "page_number": page_number_1_indexed,
                "has_images": content_analysis["has_visual_elements"],
                "content_type": content_analysis["content_type"],
                "content_description": content_analysis["content_description"],
                "is_visual_reference": content_analysis["content_type"] == "visual_heavy"
            })
    
    doc.close()
    
    print(f"\nProcessing complete:")
    print(f"  Total pages: {total_pages}")
    print(f"  Skipped pages: {len(skipped_pages)} {skipped_pages[:10]}{'...' if len(skipped_pages) > 10 else ''}")
    print(f"  Visual-heavy pages (with reference placeholders): {len(visual_heavy_pages)}")
    print(f"  Final included pages: {len(documents)}")
    
    return documents
