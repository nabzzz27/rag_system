import pytest
from src.pdf_parser import extract_text_with_metadata
import os

def test_extract_from_real_pdf():
    """Test the extraction from the actual Silat rulebook PDF."""
    pdf_path = "data/silat_rules_and_regulations_version_7.pdf"
    
    # Check if the PDF exists
    if not os.path.exists(pdf_path):
        pytest.skip(f"PDF file not found at {pdf_path}")
    
    # Extract data from the PDF
    extracted_data = extract_text_with_metadata(pdf_path)
    
    # Basic validation
    assert len(extracted_data) > 0, "Should extract at least one page"
    
    # Print information about the first 3 pages for inspection
    print(f"\n=== PDF Analysis ===")
    print(f"Total pages extracted: {len(extracted_data)}")
    print(f"===================\n")
    
    for i, page_data in enumerate(extracted_data[:3]):  # Only first 3 pages
        print(f"--- PAGE {page_data['page_number']} ---")
        print(f"Has images: {page_data['has_images']}")
        print(f"Text length: {len(page_data['text'])} characters")
        print(f"Text preview (first 200 chars):")
        print(repr(page_data['text'][:200]))
        print(f"Text preview (readable):")
        print(page_data['text'][:200])
        print("-" * 50)
    
    # Validate structure of each page
    for page_data in extracted_data[:5]:  # Check first 5 pages
        assert 'text' in page_data, "Each page should have 'text' field"
        assert 'page_number' in page_data, "Each page should have 'page_number' field"
        assert 'has_images' in page_data, "Each page should have 'has_images' field"
        assert isinstance(page_data['page_number'], int), "Page number should be integer"
        assert isinstance(page_data['has_images'], bool), "has_images should be boolean"
        assert page_data['page_number'] > 0, "Page numbers should be 1-indexed"

def test_page_numbering_sequence():
    """Test that page numbers are sequential starting from 1."""
    pdf_path = "data/silat_rules_and_regulations_version_7.pdf"
    
    if not os.path.exists(pdf_path):
        pytest.skip(f"PDF file not found at {pdf_path}")
    
    extracted_data = extract_text_with_metadata(pdf_path)
    
    # Check first 10 pages have correct sequential numbering
    for i, page_data in enumerate(extracted_data[:10]):
        expected_page_num = i + 1
        assert page_data['page_number'] == expected_page_num, \
            f"Page {i} should have page_number {expected_page_num}, got {page_data['page_number']}"

def test_image_detection():
    """Test that image detection works on real PDF."""
    pdf_path = "data/silat_rules_and_regulations_version_7.pdf"
    
    if not os.path.exists(pdf_path):
        pytest.skip(f"PDF file not found at {pdf_path}")
    
    extracted_data = extract_text_with_metadata(pdf_path)
    
    # Count pages with and without images
    pages_with_images = sum(1 for page in extracted_data if page['has_images'])
    pages_without_images = len(extracted_data) - pages_with_images
    
    print(f"\n=== Image Detection Results ===")
    print(f"Total pages: {len(extracted_data)}")
    print(f"Pages with images: {pages_with_images}")
    print(f"Pages without images: {pages_without_images}")
    
    # Show first few pages that have images
    print(f"\nFirst 5 pages with images:")
    count = 0
    for page in extracted_data:
        if page['has_images'] and count < 5:
            print(f"  Page {page['page_number']}: has images")
            count += 1
