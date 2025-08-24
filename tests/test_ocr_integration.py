import pytest
from src.pdf_parser import extract_text_with_metadata, ocr_page_images
import fitz
import os
import json

def test_ocr_quality_assessment():
    """Test OCR capability and provide manual review data."""
    pdf_path = "data/silat_rules_and_regulations_version_7.pdf"
    
    if not os.path.exists(pdf_path):
        pytest.skip(f"PDF file not found at {pdf_path}")
    
    # Extract with OCR
    extracted_data = extract_text_with_metadata(pdf_path)
    
    # Find pages where OCR was applied
    ocr_pages = [page for page in extracted_data if page.get('ocr_applied', False)]
    
    print(f"\n{'='*80}")
    print(f"OCR QUALITY ASSESSMENT")
    print(f"{'='*80}")
    print(f"Total pages processed: {len(extracted_data)}")
    print(f"Pages where OCR was applied: {len(ocr_pages)}")
    
    # Show detailed results for first 10 OCR pages
    print(f"\nDETAILED OCR RESULTS (first 10 pages):")
    print(f"{'='*80}")
    
    review_data = []
    
    for i, page_data in enumerate(ocr_pages[:10]):
        page_num = page_data['page_number']
        text_length = len(page_data['text'])
        
        print(f"\nPAGE {page_num} (OCR Applied)")
        print(f"{'-'*60}")
        print(f"Text length: {text_length} characters")
        print(f"Has images: {page_data['has_images']}")
        print(f"Content preview:")
        print(f"{page_data['text'][:500]}...")
        if len(page_data['text']) > 500:
            print(f"[...{text_length - 500} more characters...]")
        
        # Store for manual review
        review_data.append({
            'page_number': page_num,
            'text_length': text_length,
            'full_text': page_data['text'],
            'has_images': page_data['has_images']
        })
    
    # Save review data to file for manual inspection
    review_file = "ocr_review_sample.json"
    with open(review_file, 'w', encoding='utf-8') as f:
        json.dump(review_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*80}")
    print(f"OCR QUALITY REVIEW")
    print(f"{'='*80}")
    print(f"Sample OCR results saved to: {review_file}")
    print(f"Please manually review the OCR quality by examining:")
    print(f"1. Are table structures preserved?")
    print(f"2. Are numbers correctly recognized?")
    print(f"3. Are there obvious OCR errors (l vs 1, O vs 0, etc.)?")
    print(f"4. Is the extracted text meaningful and complete?")
    
    # Basic validation
    assert len(extracted_data) > 0, "Should extract some pages"
    assert len(ocr_pages) > 0, "Should have attempted OCR on some pages"
    
    # Clean up
    if os.path.exists(review_file):
        print(f"\nReview file created: {review_file}")

def test_specific_page_ocr():
    """Test OCR on a specific page we know has image-based text."""
    pdf_path = "data/silat_rules_and_regulations_version_7.pdf"
    
    if not os.path.exists(pdf_path):
        pytest.skip(f"PDF file not found at {pdf_path}")
    
    # You can specify a specific page number that you know has tables/forms
    target_page = 53  # Based on your image, adjust as needed
    
    doc = fitz.open(pdf_path)
    if target_page <= len(doc):
        page = doc.load_page(target_page - 1)  # 0-indexed
        
        pdf_text = page.get_text()
        ocr_text = ocr_page_images(page, doc)
        
        print(f"\nSPECIFIC PAGE OCR TEST - Page {target_page}")
        print(f"{'='*60}")
        print(f"PDF layer text length: {len(pdf_text)}")
        print(f"OCR text length: {len(ocr_text)}")
        print(f"\nPDF layer text:")
        print(f"{pdf_text[:200]}...")
        print(f"\nOCR extracted text:")
        print(f"{ocr_text[:500]}...")
        
        assert isinstance(ocr_text, str), "OCR should return a string"
    
    doc.close()
