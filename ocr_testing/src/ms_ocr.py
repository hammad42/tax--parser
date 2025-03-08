import time
import os
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from typing import Dict, List, Any

def perform_ocr(image_path: str) -> List[Dict[str, Any]]:
    """
    Performs OCR on the given image and extracts text.

    Args:
        image_path: The path to the image file.

    Returns:
        A list of dictionaries, where each dictionary contains extracted text and bounding box information.
        Returns an empty list on error.
    """
    azure_endpoint = os.environ.get('AZURE_ENDPOINT')
    azure_key = os.environ.get('AZURE_KEY')

    if not azure_endpoint or not azure_key:
        print("Error: Azure Endpoint or Key not found in environment variables.")
        return []

    try:
        client = ComputerVisionClient(azure_endpoint, CognitiveServicesCredentials(azure_key))

        with open(image_path, "rb") as image_file:
            response = client.read_in_stream(image_file, raw=True)

        operation_location = response.headers["Operation-Location"]
        operation_id = operation_location.split("/")[-1]

        while True:
            result = client.get_read_result(operation_id)
            if result.status.lower() not in ['notstarted', 'running']:
                break
            time.sleep(0.1) #increased sleep time.

        result = client.get_read_result(operation_id)
        return _extract_text_from_new_format(result.as_dict())

    except FileNotFoundError:
        print(f"Error: Image file not found at {image_path}")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def _extract_text_from_new_format(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Extracts text and bounding box information from the OCR result.

    Args:
        data: The OCR result as a dictionary.

    Returns:
        A list of dictionaries, where each dictionary contains extracted text and bounding box information.
    """
    extracted_data_lst: List[Dict[str, Any]] = []

    for page in data.get('analyze_result', {}).get('read_results', []):
        for line in page.get('lines', []):
            item: Dict[str, Any] = {}
            item['bounding_box'] = [
                [line['bounding_box'][0], line['bounding_box'][1]],
                [line['bounding_box'][2], line['bounding_box'][3]],
                [line['bounding_box'][4], line['bounding_box'][5]],
                [line['bounding_box'][6], line['bounding_box'][7]]
            ]
            item['text'] = line['text']
            item['confidence'] = min(word['confidence'] for word in line.get('words', [])) if line.get('words') else 1.0
            extracted_data_lst.append(item)

    return extracted_data_lst

if __name__ == "__main__":
    image_file_path = r"E:\Projects\OCR\ocr_testing\samples\color_images\Screenshot_20250211-235442_1.png"
    extracted_texts = perform_ocr(image_file_path)
    print(extracted_texts)