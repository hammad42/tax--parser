
import pandas as pd
import json
from typing import List, Dict, Any, Tuple

def get_bbox_center(bbox: List[Tuple[int, int]]) -> Tuple[float, float]:
    """Calculate the center point of a bounding box."""
    x_coords = [point[0] for point in bbox]
    y_coords = [point[1] for point in bbox]
    center_x = sum(x_coords) / 4
    center_y = sum(y_coords) / 4
    return center_x, center_y

def parse_ocr_json(ocr_data: List[Dict[str, Any]], user_keys: List[str]) -> pd.DataFrame:
    """
    Parses OCR data to extract key-value pairs based on user-defined keys.

    Args:
        ocr_data: A list of dictionaries, where each dictionary represents an OCR item
                  with 'text', 'bounding_box', and 'confidence'.
        user_keys: A list of strings representing the keys to extract.

    Returns:
        A pandas DataFrame containing the extracted key-value pairs.
    """
    if not user_keys:
        return pd.DataFrame()

    data = {key: "" for key in user_keys}
    ocr_items = []

    # Store all OCR items with their centers
    for item in ocr_data:
        center_x, center_y = get_bbox_center(item["bounding_box"])
        ocr_items.append((item["text"], center_x, center_y, item["confidence"]))

    # Sort items by y-coordinate (top to bottom) and then x-coordinate (left to right)
    ocr_items.sort(key=lambda x: (x[2], x[1]))

    # Match keys and values based on proximity
    i = 0
    while i < len(ocr_items):
        text, center_x, center_y, confidence = ocr_items[i]
        text = text.strip()

        # Check if the text matches a user-defined key
        key_matched = False
        for key in user_keys:
            if text.replace(" ", "").lower().startswith(key.lower()) or text.replace(":", "").strip().lower() == key.lower():
                key_matched = True
                # Look for the next text item as the value
                j = i + 1
                while j < len(ocr_items) and not ocr_items[j][0].strip().endswith(':'):
                    value_text, value_x, value_y, value_confidence = ocr_items[j]
                    # Check if the value is likely below or to the right of the key
                    if value_y > center_y or (abs(value_y - center_y) < 50 and value_x > center_x):
                        data[key] = value_text
                        i = j  # Move past the value
                        break
                    j += 1
                break
        
        i += 1

    df = pd.DataFrame([data])
    df = df.fillna('')

    try:
        # Check if the output file already exists and has content
        existing_df = pd.read_csv("output_ms_ocr.csv")
        append = not existing_df.empty
    except (FileNotFoundError, pd.errors.EmptyDataError):
        append = False
        
    if append:
        df.to_csv("output_ms_ocr.csv", mode='a', header=False, index=False)
    else:
        df.to_csv("output_ms_ocr.csv", index=False, columns=user_keys)

    return df
    

if __name__=="__main__":
    # This is an example of how to use the parse_ocr_json function.
    # You can replace the data_ and user_keys with your own data.
    data_ = '[{"bounding_box":[[24,3],[167,3],[167,18],[24,18]],"text":"InvoiceNumber","confidence":0.99},{"bounding_box":[[23,37],[209,37],[209,52],[23,52]],"text":"12345","confidence":0.99}]'
    data_ = json.loads(data_)
    user_keys = ["InvoiceNumber"]
    df = parse_ocr_json(data_, user_keys)
    print(df)

