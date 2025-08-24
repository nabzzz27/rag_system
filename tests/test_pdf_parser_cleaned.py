import pytest
from src.pdf_parser import extract_text_with_metadata, clean_text, filter_page
import os

def test_text_cleaning():
    """Test that boilerplate text is properly removed."""
    sample_text_with_boilerplate = """
    Some important content about silat rules.
    
    Copyright © 09 October 2023 Version 7 by International Pencak Silat Federation (PERSILAT). All rights reserved.
    No part of this material/publication may be reproduced or published in any manner without the consent in writing.
    
    More content here.
    """
    
    cleaned = clean_text(sample_text_with_boilerplate)
    
    # Check that copyright text is removed
    assert "Copyright ©" not in cleaned
    assert "All rights reserved" not in cleaned
    assert "No part of this material" not in cleaned
    
    # Check that actual content remains
    assert "Some important content about silat rules" in cleaned
    assert "More content here" in cleaned

def test_page_filtering():
    """Test page filtering logic."""
    # Test skipping configured pages (1-14 based on your config)
    assert not filter_page(1, "Some content")  # Page 1 should be skipped
    assert not filter_page(5, "Some content")  # Page 5 should be skipped
    assert not filter_page(14, "Some content") # Page 14 should be skipped
    
    # Test pages that should not be skipped
    assert filter_page(15, "Some content")  # Page 15 should not be skipped
    assert filter_page(50, "Some content")  # Page 50 should not be skipped
    
    # Test minimum length threshold (now 10 characters)
    assert not filter_page(20, "Short")  # Too short (5 chars), should be skipped
    assert filter_page(20, "This is longer")  # Long enough (14 chars), should pass

def test_cleaned_pdf_extraction():
    """Test extraction with cleaning on the real PDF."""
    pdf_path = "data/silat_rules_and_regulations_version_7.pdf"
    
    if not os.path.exists(pdf_path):
        pytest.skip(f"PDF file not found at {pdf_path}")
    
    # Extract with cleaning
    extracted_data = extract_text_with_metadata(pdf_path)
    
    print(f"\n=== CLEANED EXTRACTION RESULTS ===")
    print(f"Total pages after cleaning: {len(extracted_data)}")
    
    # Check first few pages
    print(f"\nFirst 3 pages after cleaning:")
    for i, page_data in enumerate(extracted_data[:3]):
        page_num = page_data['page_number']
        text_length = len(page_data['text'])
        has_copyright = "Copyright ©" in page_data['text']
        
        print(f"Page {page_num}: {text_length} chars, Has copyright: {has_copyright}")
        print(f"Preview: {page_data['text'][:200]}...")
        print("-" * 40)
    
    # Verify no copyright text remains
    for page_data in extracted_data[:10]:  # Check first 10 pages
        assert "Copyright ©" not in page_data['text'], f"Copyright found on page {page_data['page_number']}"
        assert "All rights reserved" not in page_data['text'], f"Rights text found on page {page_data['page_number']}"
    
    # Basic structure validation
    assert len(extracted_data) > 0, "Should have at least some pages after cleaning"
    for page in extracted_data[:5]:
        assert len(page['text']) >= 10, f"Page {page['page_number']} should have sufficient content after cleaning"
        assert page['page_number'] >= 15, f"Page {page['page_number']} should be >= 15 (after skipping first 14 pages)"
