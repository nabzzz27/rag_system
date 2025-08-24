import pytest
from src.pdf_parser import extract_text_with_metadata
import os

def test_comprehensive_pdf_analysis():
    """Comprehensive analysis of the Silat rulebook PDF - first 5, middle 5, and last 5 pages."""
    pdf_path = "data/silat_rules_and_regulations_version_7.pdf"
    
    # Check if the PDF exists
    if not os.path.exists(pdf_path):
        pytest.skip(f"PDF file not found at {pdf_path}")
    
    # Extract data from the PDF
    print("Extracting data from PDF... This may take a moment for a large PDF.")
    extracted_data = extract_text_with_metadata(pdf_path)
    
    total_pages = len(extracted_data)
    print(f"\n{'='*80}")
    print(f"COMPREHENSIVE PDF ANALYSIS")
    print(f"{'='*80}")
    print(f"Total pages extracted: {total_pages}")
    
    # Calculate middle pages
    middle_start = max(0, (total_pages // 2) - 2)
    middle_end = min(total_pages, middle_start + 5)
    
    # Define the sections to analyze
    sections = [
        ("FIRST 5 PAGES", extracted_data[:5]),
        ("MIDDLE 5 PAGES", extracted_data[middle_start:middle_end]),
        ("LAST 5 PAGES", extracted_data[-5:])
    ]
    
    for section_name, pages in sections:
        print(f"\n{'='*80}")
        print(f"{section_name}")
        print(f"{'='*80}")
        
        for page_data in pages:
            page_num = page_data['page_number']
            has_images = page_data['has_images']
            text = page_data['text']
            
            print(f"\n{'-'*60}")
            print(f"PAGE {page_num}")
            print(f"{'-'*60}")
            print(f"Has images: {has_images}")
            print(f"Text length: {len(text)} characters")
            print(f"Text content:")
            print(f"{'-'*40}")
            
            if text.strip():
                # Print the full text content, but limit extremely long pages
                if len(text) > 5000:
                    print(text[:2500])
                    print(f"\n... [TRUNCATED - showing first 2500 of {len(text)} characters] ...")
                    print(text[-2500:])
                else:
                    print(text)
            else:
                print("[NO TEXT CONTENT OR EMPTY PAGE]")
            
            print(f"{'-'*40}")
    
    # Summary statistics
    pages_with_images = sum(1 for page in extracted_data if page['has_images'])
    pages_with_text = sum(1 for page in extracted_data if page['text'].strip())
    
    print(f"\n{'='*80}")
    print(f"SUMMARY STATISTICS")
    print(f"{'='*80}")
    print(f"Total pages: {total_pages}")
    print(f"Pages with images: {pages_with_images} ({pages_with_images/total_pages*100:.1f}%)")
    print(f"Pages with text: {pages_with_text} ({pages_with_text/total_pages*100:.1f}%)")
    print(f"Average text length: {sum(len(p['text']) for p in extracted_data)/total_pages:.1f} characters")
    
    # Show some pages with images for reference
    print(f"\nFirst 10 pages with images:")
    image_count = 0
    for page in extracted_data:
        if page['has_images'] and image_count < 10:
            print(f"  Page {page['page_number']}: {len(page['text'])} characters of text")
            image_count += 1
    
    # Basic validation
    assert total_pages > 0, "Should extract at least one page"
    assert all('text' in page for page in extracted_data), "All pages should have text field"
    assert all('page_number' in page for page in extracted_data), "All pages should have page_number field"
    assert all('has_images' in page for page in extracted_data), "All pages should have has_images field"
