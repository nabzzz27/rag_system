import pytest
from src.pdf_parser import extract_text_with_metadata, clean_text, filter_page
from src.config import PAGES_TO_SKIP, MIN_TEXT_LENGTH_THRESHOLD
import fitz
import os

def test_detailed_skip_analysis():
    """Detailed analysis of which pages are skipped and why."""
    pdf_path = "data/silat_rules_and_regulations_version_7.pdf"
    
    if not os.path.exists(pdf_path):
        pytest.skip(f"PDF file not found at {pdf_path}")
    
    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    
    skipped_explicit = []  # Pages skipped due to PAGES_TO_SKIP
    skipped_length = []    # Pages skipped due to MIN_TEXT_LENGTH_THRESHOLD
    skipped_empty = []     # Pages skipped due to empty content after cleaning
    included_pages = []    # Pages that were included
    
    print(f"\n{'='*80}")
    print(f"DETAILED SKIP ANALYSIS")
    print(f"{'='*80}")
    print(f"Total pages in PDF: {total_pages}")
    print(f"Explicit skip list (PAGES_TO_SKIP): {PAGES_TO_SKIP}")
    print(f"Minimum text length threshold: {MIN_TEXT_LENGTH_THRESHOLD}")
    print(f"{'='*80}")
    
    for page_num, page in enumerate(doc):
        page_number_1_indexed = page_num + 1
        text = page.get_text()
        cleaned_text = clean_text(text)
        
        # Determine why this page was skipped (if it was)
        if page_number_1_indexed in PAGES_TO_SKIP:
            skipped_explicit.append({
                'page': page_number_1_indexed,
                'reason': 'explicit_skip',
                'original_length': len(text),
                'cleaned_length': len(cleaned_text),
                'preview': cleaned_text[:100] if cleaned_text else '[EMPTY]'
            })
        elif len(cleaned_text.strip()) < MIN_TEXT_LENGTH_THRESHOLD:
            skipped_length.append({
                'page': page_number_1_indexed,
                'reason': 'too_short',
                'original_length': len(text),
                'cleaned_length': len(cleaned_text),
                'preview': cleaned_text[:100] if cleaned_text else '[EMPTY]'
            })
        elif not cleaned_text:
            skipped_empty.append({
                'page': page_number_1_indexed,
                'reason': 'empty_after_cleaning',
                'original_length': len(text),
                'cleaned_length': len(cleaned_text),
                'preview': '[EMPTY AFTER CLEANING]'
            })
        else:
            included_pages.append({
                'page': page_number_1_indexed,
                'original_length': len(text),
                'cleaned_length': len(cleaned_text),
                'has_images': bool(page.get_images(full=True) or page.get_drawings())
            })
    
    doc.close()
    
    # Print detailed results
    print(f"\nSUMMARY:")
    print(f"- Skipped due to explicit list: {len(skipped_explicit)} pages")
    print(f"- Skipped due to length threshold: {len(skipped_length)} pages")
    print(f"- Skipped due to empty after cleaning: {len(skipped_empty)} pages")
    print(f"- Included: {len(included_pages)} pages")
    print(f"- Total: {len(skipped_explicit) + len(skipped_length) + len(skipped_empty) + len(included_pages)} pages")
    
    # Show explicit skips
    if skipped_explicit:
        print(f"\nEXPLICIT SKIPS ({len(skipped_explicit)} pages):")
        for item in skipped_explicit:
            print(f"  Page {item['page']}: {item['cleaned_length']} chars - {item['preview']}")
    
    # Show length-based skips (first 20)
    if skipped_length:
        print(f"\nLENGTH-BASED SKIPS ({len(skipped_length)} pages, showing first 20):")
        for item in skipped_length[:20]:
            print(f"  Page {item['page']}: {item['cleaned_length']} chars - {item['preview']}")
        if len(skipped_length) > 20:
            print(f"  ... and {len(skipped_length) - 20} more pages")
    
    # Show empty after cleaning
    if skipped_empty:
        print(f"\nEMPTY AFTER CLEANING ({len(skipped_empty)} pages):")
        for item in skipped_empty:
            print(f"  Page {item['page']}: {item['preview']}")
    
    # Show first few included pages for reference
    print(f"\nFIRST 5 INCLUDED PAGES:")
    for item in included_pages[:5]:
        print(f"  Page {item['page']}: {item['cleaned_length']} chars, has_images: {item['has_images']}")
    
    # Create comprehensive lists for your review
    all_skipped = [item['page'] for item in skipped_explicit + skipped_length + skipped_empty]
    all_skipped.sort()
    
    print(f"\nCOMPLETE LIST OF ALL SKIPPED PAGES ({len(all_skipped)} total):")
    print(f"Pages: {all_skipped}")
    
    # Group consecutive pages for easier reading
    def group_consecutive(pages):
        if not pages:
            return []
        
        groups = []
        start = pages[0]
        end = pages[0]
        
        for i in range(1, len(pages)):
            if pages[i] == end + 1:
                end = pages[i]
            else:
                if start == end:
                    groups.append(str(start))
                else:
                    groups.append(f"{start}-{end}")
                start = end = pages[i]
        
        if start == end:
            groups.append(str(start))
        else:
            groups.append(f"{start}-{end}")
        
        return groups
    
    grouped_skipped = group_consecutive(all_skipped)
    print(f"\nSKIPPED PAGES (grouped): {', '.join(grouped_skipped)}")
    
    # Verify our math
    expected_total = len(included_pages) + len(all_skipped)
    assert expected_total == total_pages, f"Math error: {expected_total} != {total_pages}"
