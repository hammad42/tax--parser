from paddleocr import PaddleOCR, draw_ocr # main OCR dependencies
from matplotlib import pyplot as plt # plot images
import cv2 #opencv
import os # folder directory navigation

ocr_model= PaddleOCR(use_gpu=True,lang='en') # Load the OCR model
result = ocr_model.ocr(r'E:\Projects\OCR\ocr_testing\gray_images\gray_test.jpg')
# print(result)
# with open(r'E:\Projects\tax_parser\testing\output.txt', 'w') as f:
#         f.write(str(result))
def extract_text(data):
  """
  Extracts text from the given nested list data structure.

  Args:
    data: A nested list containing text and bounding box information.

  Returns:
    A list of strings containing the extracted text.
  """
  extracted_texts = []
  for item_level1 in data:
    for item_level2 in item_level1:
      if isinstance(item_level2, tuple):
        text = item_level2[0]
        extracted_texts.append(text)
  return extracted_texts

texts = extract_text(result[0])
with open(r'E:\Projects\OCR\ocr_testing\output_grey.txt', 'w') as f:
  f.write(str(texts))