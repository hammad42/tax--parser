import src.ms_ocr as ms_ocr
import src.paddle_ocr as p_ocr
from typing import List, Dict, Any, Union, BinaryIO


def perform_ocr(image: Union[str, bytes, BinaryIO], ocr_tool: str) -> List[Dict[str, Any]]:
    """
    Performs OCR on the given image using the specified OCR tool.

    Args:
        image: The path to the image file, image as bytes, or a file-like object.
        ocr_tool: The OCR tool to use. Can be "azure" or "paddle".

    Returns:
        A list of dictionaries, where each dictionary contains extracted text and bounding box information.
        Returns an empty list on error.
    """

    if ocr_tool not in ["azure", "paddle"]:
        raise ValueError("Invalid OCR tool specified. Choose either 'azure' or 'paddle'.")

    if ocr_tool == "azure":
        return ms_ocr.perform_ocr(image)
    elif ocr_tool == "paddle":
        return p_ocr.perform_paddle_ocr(image)


if __name__ == "__main__":
    image_path = r"E:\Projects\OCR\ocr_testing\samples\color_images\Screenshot_20250211-234427_1.png"
    ocr_tool = "azure"
    results = perform_ocr(image_path, "paddle")
    print(results)