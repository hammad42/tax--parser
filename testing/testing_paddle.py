from paddleocr import PaddleOCR, draw_ocr # main OCR dependencies
from matplotlib import pyplot as plt # plot images
import cv2 #opencv
import os # folder directory navigation

ocr_model= PaddleOCR(use_gpu=True,lang='en') # Load the OCR model
result = ocr_model.ocr(r'E:\Projects\tax_parser\testing\test.jpg')
# print(result)
# with open(r'E:\Projects\tax_parser\testing\output.txt', 'w') as f:
#         f.write(str(result))
for line in result:
    print(line[1][0])