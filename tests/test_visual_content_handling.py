import pytest
from src.pdf_parser import extract_text_with_metadata
import os
import json

def test_visual_content_handling():
    """Test the improved visual content handling approach."""
    pdf_path = "data/silat_rules_and_regulations_version_7.pdf"
    
    if not os.path.exists(pdf_path):
        pytest.skip(f"PDF file not found at {pdf_path}")
    
    # Extract with improved visual handling
    extracted_data = extract_text_with_metadata(pdf_path)
    
    # Analyze results
    visual_reference_pages = [page for page in extracted_data if page.get('is_visual_reference', False)]
    text_pages = [page for page in extracted_data if not page.get('is_visual_reference', False)]
    
    print(f"\n{'='*80}")
    print(f"IMPROVED VISUAL CONTENT HANDLING RESULTS")
    print(f"{'='*80}")
    print(f"Total pages processed: {len(extracted_data)}")
    print(f"Text-based pages: {len(text_pages)}")
    print(f"Visual reference pages: {len(visual_reference_pages)}")
    
    # Show examples of visual reference pages
    print(f"\nVISUAL REFERENCE PAGES (first 5):")
    print(f"{'='*80}")
    
    for i, page_data in enumerate(visual_reference_pages[:5]):
        page_num = page_data['page_number']
        description = page_data['content_description']
        
        print(f"\nPAGE {page_num}")
        print(f"{'-'*40}")
        print(f"Content Type: {page_data['content_type']}")
        print(f"Description: {description}")
        print(f"Reference Text Preview:")
        print(f"{page_data['text'][:300]}...")
        print(f"{'='*40}")
    
    # Save sample for review
    sample_data = {
        'summary': {
            'total_pages': len(extracted_data),
            'text_pages': len(text_pages),
            'visual_reference_pages': len(visual_reference_pages)
        },
        'visual_reference_samples': visual_reference_pages[:10]
    }
    
    with open('visual_content_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(sample_data, f, indent=2, ensure_ascii=False)
    
    print(f"\nAnalysis saved to: visual_content_analysis.json")
    
    # Test that visual pages have meaningful content
    for page in visual_reference_pages[:5]:
        assert "VISUAL CONTENT REFERENCE" in page['text']
        assert f"page {page['page_number']}" in page['text'].lower()
        assert len(page['text']) > 100  # Should have substantial reference text
    
    print(f"\n{'='*80}")
    print(f"ADVANTAGES OF THIS APPROACH:")
    print(f"{'='*80}")
    print(f"✓ No more OCR gibberish")
    print(f"✓ Clear user guidance to check specific pages")  
    print(f"✓ Searchable keywords for visual content")
    print(f"✓ Maintains page references for linking")
    print(f"✓ RAG system can direct users to original PDF pages")
