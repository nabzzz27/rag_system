import fitz
from typing import Dict, Any

def analyze_page_content(page: fitz.Page, text_content: str) -> Dict[str, Any]:
    """
    Analyze a page to determine what type of content it contains.
    Returns metadata about the page content type.
    """
    text_length = len(text_content.strip())
    images = page.get_images(full=True)
    drawings = page.get_drawings()
    
    # Count visual elements
    image_count = len(images)
    drawing_count = len(drawings)
    has_visual_elements = image_count > 0 or drawing_count > 0
    
    # Determine content type based on text-to-visual ratio
    content_type = "unknown"
    content_description = ""
    
    if text_length > 200 and not has_visual_elements:
        content_type = "text_only"
        content_description = "Text content"
    elif text_length > 200 and has_visual_elements:
        content_type = "mixed_content"
        content_description = f"Text with {image_count} images and {drawing_count} diagrams"
    elif text_length < 50 and has_visual_elements:
        content_type = "visual_heavy"
        if image_count > 0 and drawing_count > 0:
            content_description = f"Primarily visual content: {image_count} images and {drawing_count} diagrams - likely contains tables, forms, or structured layouts"
        elif image_count > 0:
            content_description = f"Primarily visual content: {image_count} images - likely contains tables, forms, or structured layouts"
        else:
            content_description = f"Primarily visual content: {drawing_count} diagrams - likely contains charts or technical drawings"
    elif text_length < 50 and not has_visual_elements:
        content_type = "minimal_content"
        content_description = "Minimal content - possibly blank or section divider"
    else:
        content_type = "balanced"
        content_description = f"Balanced content with text and {image_count + drawing_count} visual elements"
    
    return {
        "content_type": content_type,
        "content_description": content_description,
        "text_length": text_length,
        "image_count": image_count,
        "drawing_count": drawing_count,
        "has_visual_elements": has_visual_elements
    }

def create_visual_content_placeholder(page_number: int, content_analysis: Dict[str, Any]) -> str:
    """
    Creates a meaningful text placeholder for pages with primarily visual content.
    This text will be indexed and can be found during retrieval.
    """
    content_type = content_analysis["content_type"]
    description = content_analysis["content_description"]
    
    if content_type == "visual_heavy":
        # Create searchable text that describes what's likely on this page
        placeholder_text = f"""
PAGE {page_number} VISUAL CONTENT REFERENCE

This page contains primarily visual elements: {description}

CONTENT TYPE: Structured visual content (tables, forms, diagrams)
IMAGES: {content_analysis['image_count']} image(s)
DIAGRAMS: {content_analysis['drawing_count']} diagram(s)

NOTE: This page likely contains important structured information such as:
- Rules tables or matrices
- Scoring forms or checklists  
- Technical diagrams or illustrations
- Competition formats or brackets
- Reference charts or quick-lookup tables

For complete and accurate information from this page, please refer directly to page {page_number} in the original PDF document, as it contains structured visual content that is best viewed in its original format.

SEARCH KEYWORDS: visual content, table, form, diagram, chart, structured layout, page {page_number}
"""
    else:
        placeholder_text = f"""
PAGE {page_number} CONTENT REFERENCE

{description}

NOTE: This page contains visual elements that may include important diagrams, tables, or forms. 
Please refer to page {page_number} in the original PDF for complete visual information.
"""
    
    return placeholder_text.strip()
