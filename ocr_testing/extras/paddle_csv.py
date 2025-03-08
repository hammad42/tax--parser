from paddleocr import PaddleOCR
import os
import pandas as pd

ocr_model = PaddleOCR(use_gpu=True, lang='en')  # Initialize OCR model globally

# Define expected keys based on previous analysis
EXPECTED_KEYS = [
    "Invoice Number", "Total Sales Value", "Total Quantity",
    "Total Tax Charged", "Discount", "Total Bill Amount",
    "Date Time", "NTN", "Business Name", "Branch Name",
    "Branch Address", "POS Counter"
]

def perform_ocr_and_save_csv(image_path_or_folder, output_csv="ocr_results.csv"):
    """
    Performs OCR on images in a folder and saves the results to a CSV file.
    """
    image_paths = []
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
    
    data_list = []
    
    for image_path in image_paths:
        try:
            result = ocr_model.ocr(image_path, cls=False)  # Perform OCR
            text_results = [" ".join([word_info[1][0] for word_info in line]) for line in result]
            
            # Create dictionary to map extracted text to expected keys
            extracted_data = {key: "" for key in EXPECTED_KEYS}
            
            for key in EXPECTED_KEYS:
                for text in text_results:
                    if key.lower() in text.lower():
                        extracted_data[key] = text.split(key, 1)[-1].strip()
                        break  # Assign first found value
            
            data_list.append(extracted_data)
            
        except Exception as e:
            print(f"Error during OCR processing of {image_path}: {e}")
            continue
    
    # Convert to DataFrame and save to CSV
    df = pd.DataFrame(data_list)
    df.to_csv(output_csv, index=False)
    print(f"OCR results saved to {output_csv}")
    
    return output_csv

if __name__ == "__main__":
    image_path_or_folder = r'samples/gray_images/'  # Modify with actual path
    output_csv_path = "ocr_results.csv"
    perform_ocr_and_save_csv(image_path_or_folder, output_csv_path)