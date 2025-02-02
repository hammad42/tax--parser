import pytesseract
from PIL import Image

# Path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'E:\Projects\tessaract\tesseract.exe'

# Path to the image file
image_path = r'E:\Projects\tax_parser\testing\Screenshot_20250202_163649_Tax Asaan.jpg'

# Open the image file
image = Image.open(image_path)

# Use pytesseract to do OCR on the image
text = pytesseract.image_to_string(image)

# Print the extracted text
print(text)
print("Done")