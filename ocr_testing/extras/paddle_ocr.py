from paddleocr import PaddleOCR
import cv2
import numpy as np
import os

ocr_model = PaddleOCR(use_gpu=True, lang='en')  # Initialize OCR model globally



def perform_ocr_and_draw(image_path_or_folder, output_folder="outputs\color_outputs"):
    """
    Performs OCR on an image or a folder of images and draws bounding boxes and text.

    Args:
        image_path_or_folder: Path to a single image or a folder containing images.
        output_folder: Path to the output folder.

    Returns:
        A list of paths to the saved OCR'd images, or None if an error occurred.
    """

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    saved_paths = []

    if os.path.isfile(image_path_or_folder):
        image_paths = [image_path_or_folder]
    elif os.path.isdir(image_path_or_folder):
        image_paths = [
            os.path.join(image_path_or_folder, filename)
            for filename in os.listdir(image_path_or_folder)
            if os.path.isfile(os.path.join(image_path_or_folder, filename))
        ]
    else:
        print(f"Error: Invalid path: {image_path_or_folder}")
        return None

    for image_path in image_paths:
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error: Could not read image at {image_path}")
            continue

        try:
            result = ocr_model.ocr(image_path, cls=False)  # Perform OCR

            for line in result:
                for word_info in line:
                    bbox, text_info = word_info[:2]
                    text, confidence = text_info

                    bbox = np.array(bbox, dtype=np.int32)

                    cv2.polylines(image, [bbox], isClosed=True, color=(0, 255, 0), thickness=1)
                    text_position = (bbox[0][0], bbox[0][1] - 2)
                    cv2.putText(image, str(text_info), text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 1, cv2.LINE_AA)

            image_name = os.path.basename(image_path)
            ocr_image_name = "ocr_" + image_name
            ocr_image_path = os.path.join(output_folder, ocr_image_name)
            cv2.imwrite(ocr_image_path, image)
            print(f"OCR result saved to {ocr_image_path}")
            saved_paths.append(ocr_image_path)

        except Exception as e: # Catch any errors during OCR or drawing
            print(f"Error during OCR processing of {image_path}: {e}")
            continue # Skip to the next image

    return saved_paths

if __name__ == "__main__":
    image_path_or_folder = r'samples\gray_images\gray_Screenshot_20250211-234427_1.png'
    perform_ocr_and_draw(image_path_or_folder)
