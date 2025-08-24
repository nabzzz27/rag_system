from typing import List, Dict, Any

def display_page_samples(extracted_data: List[Dict[str, Any]], sample_size: int = 7):
    """
    Display samples from the beginning, middle, and end of the extracted data.
    """
    total_pages = len(extracted_data)
    
    if total_pages == 0:
        print("No pages to display.")
        return
    
    print(f"\n{'='*80}")
    print(f"PAGE SAMPLES ANALYSIS")
    print(f"{'='*80}")
    print(f"Total extracted pages: {total_pages}")
    print(f"Sample size: {sample_size} pages each")
    
    # Calculate indices for middle section
    middle_start = max(0, (total_pages // 2) - (sample_size // 2))
    middle_end = min(total_pages, middle_start + sample_size)
    
    # Define sections
    sections = [
        ("FIRST", extracted_data[:sample_size]),
        ("MIDDLE", extracted_data[middle_start:middle_end]),
        ("LAST", extracted_data[-sample_size:])
    ]
    
    for section_name, pages in sections:
        print(f"\n{'='*80}")
        print(f"{section_name} {len(pages)} PAGES")
        print(f"{'='*80}")
        
        for page_data in pages:
            page_num = page_data['page_number']
            content_type = page_data.get('content_type', 'unknown')
            text_length = len(page_data['text'])
            is_visual = page_data.get('is_visual_reference', False)
            
            print(f"\n{'-'*60}")
            print(f"PAGE {page_num}")
            print(f"{'-'*60}")
            print(f"Content Type: {content_type}")
            print(f"Text Length: {text_length} characters")
            print(f"Visual Reference: {'Yes' if is_visual else 'No'}")
            print(f"Has Images: {page_data.get('has_images', False)}")
            
            # Show text preview
            text_preview = page_data['text'][:300]
            if is_visual:
                print(f"\nVisual Reference Content:")
                print(f"{text_preview}...")
            else:
                print(f"\nText Content Preview:")
                print(f"{text_preview}...")
            
            if len(page_data['text']) > 300:
                print(f"[...{text_length - 300} more characters...]")
            
            print(f"{'-'*60}")

def generate_summary_stats(extracted_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate summary statistics about the extracted data."""
    total_pages = len(extracted_data)
    
    # Count by content type
    content_types = {}
    visual_references = 0
    pages_with_images = 0
    total_text_length = 0
    
    for page in extracted_data:
        content_type = page.get('content_type', 'unknown')
        content_types[content_type] = content_types.get(content_type, 0) + 1
        
        if page.get('is_visual_reference', False):
            visual_references += 1
        
        if page.get('has_images', False):
            pages_with_images += 1
        
        total_text_length += len(page['text'])
    
    return {
        'total_pages': total_pages,
        'content_types': content_types,
        'visual_references': visual_references,
        'pages_with_images': pages_with_images,
        'total_text_length': total_text_length,
        'average_text_length': total_text_length / total_pages if total_pages > 0 else 0
    }

def print_summary_stats(stats: Dict[str, Any]):
    """Print formatted summary statistics."""
    print(f"\n{'='*80}")
    print(f"EXTRACTION SUMMARY STATISTICS")
    print(f"{'='*80}")
    print(f"Total Pages: {stats['total_pages']}")
    print(f"Visual References: {stats['visual_references']}")
    print(f"Pages with Images: {stats['pages_with_images']}")
    print(f"Total Text Length: {stats['total_text_length']:,} characters")
    print(f"Average Text per Page: {stats['average_text_length']:.1f} characters")
    
    print(f"\nContent Type Breakdown:")
    for content_type, count in stats['content_types'].items():
        percentage = (count / stats['total_pages']) * 100
        print(f"  {content_type}: {count} pages ({percentage:.1f}%)")


