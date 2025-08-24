import pytest
import pytesseract
from PIL import Image
import os
from src.config import TESSERACT_PATH

def test_tesseract_installation():
    """Test that Tesseract is properly installed and accessible."""
    
    # Check if Tesseract executable exists
    assert os.path.exists(TESSERACT_PATH), f"Tesseract not found at {TESSERACT_PATH}"
    
    # Set the path
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
    
    # Try to get Tesseract version
    try:
        version = pytesseract.get_tesseract_version()
        print(f"Tesseract version: {version}")
        assert version is not None, "Could not get Tesseract version"
    except Exception as e:
        pytest.fail(f"Tesseract installation test failed: {e}")
    
    # Create a simple test image with text
    test_image = Image.new('RGB', (200, 50), color='white')
    
    # Try basic OCR (this will fail if Tesseract isn't working)
    try:
        result = pytesseract.image_to_string(test_image)
        print(f"OCR test successful. Result: '{result.strip()}'")
    except Exception as e:
        pytest.fail(f"OCR test failed: {e}")

if __name__ == "__main__":
    test_tesseract_installation()
