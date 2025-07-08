import pytesseract
from PIL import Image
import io
import os

def extract_text_from_image(image):
    """
    Extract text from an image using OCR
    """
    try:
        # Convert image to grayscale for better OCR
        if image.mode != 'L':
            image = image.convert('L')
        
        # Use Tesseract to do OCR on the image
        text = pytesseract.image_to_string(image)
        
        return text
    except Exception as e:
        print(f"Error in OCR processing: {e}")
        return "Could not extract text from the image. Please try typing the question instead."