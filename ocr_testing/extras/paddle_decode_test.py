from paddleocr import PaddleOCR, draw_ocr # main OCR dependencies
ocr_model= PaddleOCR(use_gpu=True,lang='en') # Load the OCR model
result = ocr_model.ocr(r'E:\Projects\OCR\ocr_testing\samples\gray_images\gray_Screenshot_20250211-234427_1.png', cls=False) # Run the OCR model on the image
print(result)