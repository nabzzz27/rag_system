import os
import pytest
import fitz  # PyMuPDF
from PIL import Image
from src.pdf_parser import extract_text_with_metadata

@pytest.fixture(scope="module")
def dummy_pdf_path():
    """Create a dummy PDF for testing and return its path."""
    pdf_path = "dummy_test.pdf"
    img_path = "dummy_image.png"

    # Create a dummy image
    img = Image.new('RGB', (100, 100), color = 'red')
    img.save(img_path)

    doc = fitz.open()

    # Page 1: Text only
    page1 = doc.new_page()
    page1.insert_text((50, 72), "This is the first page.", fontsize=12)

    # Page 2: Text and an image
    page2 = doc.new_page()
    page2.insert_text((50, 72), "This is the second page with an image.", fontsize=12)
    # Fix: Provide a proper rectangle (x0, y0, x1, y1) for image placement
    page2.insert_image(fitz.Rect(50, 100, 150, 200), filename=img_path)

    doc.save(pdf_path)
    doc.close()

    yield pdf_path

    # Teardown: clean up the created files
    os.remove(pdf_path)
    os.remove(img_path)

def test_extract_text_with_metadata(dummy_pdf_path):
    """Test the extraction of text and metadata from the dummy PDF."""
    extracted_data = extract_text_with_metadata(dummy_pdf_path)

    # Verify the number of pages
    assert len(extracted_data) == 2, "Should process two pages."

    # Verify Page 1 content
    page1_data = extracted_data[0]
    assert "This is the first page." in page1_data['text']
    assert page1_data['page_number'] == 1
    assert not page1_data['has_images'], "Page 1 should have no images."

    # Verify Page 2 content
    page2_data = extracted_data[1]
    assert "This is the second page with an image." in page2_data['text']
    assert page2_data['page_number'] == 2
    assert page2_data['has_images'], "Page 2 should have an image."
