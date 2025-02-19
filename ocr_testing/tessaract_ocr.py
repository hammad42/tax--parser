import pytesseract
from PIL import Image

# Path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'E:\Projects\tessaract\tesseract.exe'

# Path to the image file
image_path = r'E:\Projects\OCR\ocr_testing\gray_images\gray_test.jpg'

# Open the image file
image = Image.open(image_path)

# Use pytesseract to do OCR on the image
text = pytesseract.image_to_string(image)

# Print the extracted text
with open(r'E:\Projects\OCR\ocr_testing\tessaract_output_grey.txt', 'w') as f:
  f.write(str(text))