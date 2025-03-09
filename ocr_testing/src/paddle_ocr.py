import os
from typing import List, Dict, Any

import cv2
from paddleocr import PaddleOCR, draw_ocr
from matplotlib import pyplot as plt


def perform_paddle_ocr(image_path: str, use_gpu: bool = True, lang: str = 'en') -> List[Dict[str, Any]]:
    """
    Performs OCR using PaddleOCR on the given image and extracts text.

    Args:
        image_path: The path to the image file or in bytes.
        use_gpu: Whether to use GPU for OCR processing.
        lang: Language to use for OCR.

    Returns:
        A list of dictionaries, where each dictionary contains extracted text,
        bounding box, and confidence information. Returns an empty list on error.
    """
    try:
        ocr_model = PaddleOCR(use_gpu=use_gpu, lang=lang, show_log=False)  # Load the OCR model

        result = ocr_model.ocr(image_path, cls=False)  # Run the OCR model on the image

        return _extract_text(result)

    except FileNotFoundError:
        print(f"Error: Image file not found at {image_path}")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
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