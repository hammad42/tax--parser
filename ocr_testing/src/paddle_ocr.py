import os
from typing import List, Dict, Any, Union, BinaryIO
import numpy as np
import cv2
from paddleocr import PaddleOCR

# Global variable to hold the PaddleOCR model instance
ocr_model = None


def perform_paddle_ocr(image: Union[str, bytes, BinaryIO], use_gpu: bool = True, lang: str = 'en') -> List[Dict[str, Any]]:
    """
    Performs OCR using PaddleOCR on the given image and extracts text.

    Args:
        image: The path to the image file, image as bytes, or a file-like object.
        use_gpu: Whether to use GPU for OCR processing.
        lang: Language to use for OCR.

    Returns:
        A list of dictionaries, where each dictionary contains extracted text,
        bounding box, and confidence information. Returns an empty list on error.
    """
    global ocr_model
    try:
        # Initialize the model if it hasn't been already
        if ocr_model is None:
            ocr_model = PaddleOCR(use_gpu=use_gpu, lang=lang, show_log=False)

        img_for_ocr = None
        if isinstance(image, str):
            if not os.path.exists(image):
                print(f"Error: Image file not found at {image}")
                return []
            img_for_ocr = image  # pass path directly
        elif isinstance(image, bytes):
            nparr = np.frombuffer(image, np.uint8)
            img_for_ocr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        elif hasattr(image, 'read'):
            nparr = np.frombuffer(image.read(), np.uint8)
            img_for_ocr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        else:
            print("Error: Unsupported image input type.")
            return []

        if img_for_ocr is None and not isinstance(image, str):
            print("Error: could not decode image from bytes.")
            return []

        # Run the OCR model on the image
        result = ocr_model.ocr(img_for_ocr, cls=False)

        return _extract_text(result)

    except Exception as e:
        print(f"An error occurred in PaddleOCR: {e}")
        return []


def _extract_text(data: List[List[List[Any]]]) -> List[Dict[str, Any]]:
    """
    Extracts text from the PaddleOCR result.

    Args:
        data: The PaddleOCR result as a nested list.

    Returns:
        A list of dictionaries, where each dictionary contains extracted text,
        bounding box, and confidence information.
    """
    extracted_data_lst: List[Dict[str, Any]] = []
    if not data:
        return extracted_data_lst

    for item_level1 in data:
        for bounding_box in item_level1:
            item: Dict[str, Any] = {}
            b_box = bounding_box[0]
            item['bounding_box'] = b_box
            text = bounding_box[1][0]
            item['text'] = text
            confidence = bounding_box[1][1]
            item['confidence'] = confidence
            extracted_data_lst.append(item)
    return extracted_data_lst


if __name__ == "__main__":
    image_file_path = r"E:\Projects\OCR\ocr_testing\samples\gray_images\gray_Screenshot_20250211-234427_1.png"
    extracted_texts = perform_paddle_ocr(image_file_path)
    print(extracted_texts)