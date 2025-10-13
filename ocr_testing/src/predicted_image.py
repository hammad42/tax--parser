import cv2
import json
import numpy as np
from typing import Union, List, Dict, Any, Tuple

def draw_boxes_on_image(image: Union[str, bytes, np.ndarray], json_data: Union[str, List[Dict[str, Any]]]) -> np.ndarray:
    """
    Draws bounding boxes and text on the given image.

    Args:
        image: The input image, which can be a file path (str), image bytes, or a NumPy array.
        json_data: A JSON string or a list of dictionaries containing bounding box coordinates and text.
                   Each dictionary should have "bounding_box" and "text" keys. "confidence" is optional.

    Returns:
        A NumPy array representing the image with bounding boxes and text drawn on it.

    Raises:
        FileNotFoundError: If the image path is invalid.
        ValueError: If the image format is not supported.
    """
    if isinstance(image, str):
        img = cv2.imread(image)
        if img is None:
            raise FileNotFoundError(f"Unable to load image at {image}")
    elif isinstance(image, bytes):
        nparr = np.frombuffer(image, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("Could not decode image from bytes.")
    elif isinstance(image, np.ndarray):
        img = image
    else:
        raise TypeError("Unsupported image type. Please provide a path, bytes, or NumPy array.")
        
    if isinstance(json_data, str):
        data = json.loads(json_data)
    else:
        data = json_data

    for item in data:
        bbox: List[Tuple[int, int]] = item["bounding_box"]
        text = str(item["text"])

        if "confidence" in item:
            confidence = item.get("confidence", 0.0)
            text += f'/{confidence:.2f}'

        xs = [pt[0] for pt in bbox]
        ys = [pt[1] for pt in bbox]
        top_left = (int(min(xs)), int(min(ys)))
        bottom_right = (int(max(xs)), int(max(ys)))

        cv2.rectangle(img, top_left, bottom_right, color=(0, 255, 0), thickness=2)
        cv2.putText(img, text, (top_left[0], top_left[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(0, 0, 255), thickness=1)

    return img

# Example usage:
if __name__ == "__main__":
    # Load your image
    image = r"E:\Projects\OCR\ocr_testing\samples\color_images\Screenshot_20250211-235652_1.png"

    # Your JSON data (as provided in your example)
    json_str = [{"bounding_box":[[21,12],[172,12],[172,29],[21,29]],"text":"Invoice Number:","confidence":0.975},{"bounding_box":[[21,47],[226,47],[226,65],[21,66]],"text":"17256224121322859780","confidence":0.978},{"bounding_box":[[23,94],[183,94],[183,112],[23,112]],"text":"Total Sales Value:","confidence":0.994},{"bounding_box":[[21,130],[87,131],[87,148],[21,148]],"text":"3333.91","confidence":0.995},{"bounding_box":[[23,176],[155,177],[155,198],[23,197]],"text":"Total Quantity:","confidence":0.994},{"bounding_box":[[23,214],[61,214],[62,231],[23,230]],"text":"9.00","confidence":0.993},{"bounding_box":[[21,259],[195,260],[194,280],[21,279]],"text":"Total Tax Charged:","confidence":0.994},{"bounding_box":[[23,296],[84,296],[84,313],[23,313]],"text":"600.09","confidence":0.994},{"bounding_box":[[22,342],[108,342],[108,360],[22,360]],"text":"Discount:","confidence":0.994},{"bounding_box":[[22,379],[61,379],[61,396],[22,395]],"text":"0.00","confidence":0.993},{"bounding_box":[[22,425],[181,425],[181,443],[22,442]],"text":"Total Bill Amount:","confidence":0.989},{"bounding_box":[[21,462],[95,462],[95,479],[22,479]],"text":"3935.62","confidence":0.997},{"bounding_box":[[22,508],[122,508],[122,526],[22,525]],"text":"Date Time:","confidence":0.993},{"bounding_box":[[22,544],[262,544],[262,562],[22,562]],"text":"2024-12-13T22:05:00+05:00","confidence":0.848},{"bounding_box":[[22,592],[61,590],[62,607],[22,607]],"text":"NTN:","confidence":0.989},{"bounding_box":[[23,627],[123,627],[123,645],[23,644]],"text":"8009003-2","confidence":0.991},{"bounding_box":[[22,674],[166,675],[166,691],[21,690]],"text":"Business Name:","confidence":0.994},{"bounding_box":[[22,710],[217,710],[217,727],[22,728]],"text":"C PLUS SUPER MARKET","confidence":0.991},{"bounding_box":[[22,757],[153,757],[153,774],[22,774]],"text":"Branch Name:","confidence":0.994},{"bounding_box":[[21,790],[308,790],[308,813],[21,813]],"text":"C PLUS SUPER MARKET (UP Morr)","confidence":0.989},{"bounding_box":[[21,838],[171,839],[171,858],[21,857]],"text":"Branch Address:","confidence":0.994},{"bounding_box":[[22,873],[405,873],[405,895],[22,895]],"text":"Plot A-01 (ST-09) sector 11-1 north karachi","confidence":0.928},{"bounding_box":[[22,921],[144,922],[143,940],[22,939]],"text":"POS Counter:","confidence":0.994},{"bounding_box":[[22,957],[84,957],[84,976],[21,975]],"text":"172562","confidence":0.994}]
    
    # Draw boxes and text over image
    output_image = draw_boxes_on_image(image, json_str)
    
    # Save or display the output image
    cv2.imwrite("output_image.jpg", output_image)

