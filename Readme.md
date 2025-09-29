# OCR Project

This project is designed to extract text information from images and convert it into a structured format, such as a CSV file. The primary goal is to process images (e.g., tax documents) and extract relevant data using various OCR tools and techniques.

---

## End-to-End Process

1. **Input Images**: Provide images (e.g., tax documents) as input. These images can be in color or grayscale.
2. **Preprocessing**: Preprocess the images to enhance their quality for OCR. This includes converting images to grayscale, upscaling DPI, and other transformations.
3. **OCR Processing**: Use one of the supported OCR tools to extract text from the images. Supported tools include:
   - **Microsoft Cognitive Services (Azure OCR)**: Extracts text using Microsoft's cloud-based OCR service.
   - **PaddleOCR**: A lightweight, open-source OCR tool.
   - **Tesseract OCR**: An open-source OCR engine.
   - **AWS Textract** and **Google Vision API** (future integration).
4. **Postprocessing**: Decode and structure the extracted text into a usable format.
5. **Output**: Save the extracted and structured data into a CSV file.

---

## Tools and Libraries Used

- **Microsoft Cognitive Services**: For cloud-based OCR.
- **PaddleOCR**: For local OCR processing.
- **Tesseract OCR**: For open-source OCR.
- **OpenCV**: For image preprocessing.
- **Pandas**: For structuring and saving data into CSV format.
- **Azure SDK**: For interacting with Azure Cognitive Services.

---

## File Structure and Explanation

### **Main Files**

1. **`main.py`**:
   - The entry point of the project.
   - Handles the overall workflow, including preprocessing, OCR processing, and saving the output.
   - Allows users to select the OCR tool (e.g., Azure, PaddleOCR, or Tesseract).

2. **`output.csv`**:
   - The final output file where the extracted text is saved in a structured format.

---

### **Source Code Files (`src/`)**

1. **`bgr2grey.py`**:
   - Converts images from BGR (color) to grayscale.
   - Helps improve OCR accuracy by reducing noise in the images.

2. **`fpath.py`**:
   - Handles file path operations.
   - Retrieves file paths from a given directory or validates individual file paths.

3. **`ms_ocr.py`**:
   - Implements OCR using Microsoft Cognitive Services.
   - Sends images to Azure's OCR API and retrieves text along with bounding box information.

4. **`ocr_selection.py`**:
   - Provides a unified interface to select and use different OCR tools (e.g., Azure, PaddleOCR).
   - Acts as a bridge between the main script and individual OCR implementations.

5. **`paddle_ocr.py`**:
   - Implements OCR using PaddleOCR.
   - Processes images locally and extracts text.

6. **`predicted_image.py`**:
   - Handles visualization of OCR results.
   - Overlays extracted text and bounding boxes on the original image for verification.

7. **`structured.py`**:
   - Structures the extracted text into a tabular format.
   - Prepares the data for saving into a CSV file.

8. **`upscale_dpi.py`**:
   - Upscales the DPI (dots per inch) of images to improve OCR accuracy.
   - Useful for low-resolution images.

---

### **Extras (`extras/`)**

1. **`gpu_test.py`**:
   - Tests GPU compatibility and performance for OCR tools like PaddleOCR.

2. **`paddle_csv.py`**:
   - Converts PaddleOCR results into a CSV format.

3. **`preprocessing_image.ipynb`**:
   - A Jupyter Notebook for experimenting with image preprocessing techniques.

4. **`tessaract_ocr.py`**:
   - Implements OCR using Tesseract.
   - Processes images locally and extracts text.

5. **`upscaling.ipynb`**:
   - A Jupyter Notebook for experimenting with image upscaling techniques.

---

### **Configuration and Cache**

1. **`.gitignore`**:
   - Specifies files and folders to exclude from version control.

2. **`__pycache__/`**:
   - Contains compiled Python files for faster execution.

---

## How to Run the Project

1. **Set Up Environment**:
   - Install the required Python libraries using `pip install -r requirements.txt`.
   - Set up environment variables for Azure OCR:
     - `AZURE_ENDPOINT`: Your Azure endpoint.
     - `AZURE_KEY`: Your Azure API key.

2. **Run the Main Script**:
   - Execute `main.py` to start the OCR process:
     ```bash
     python main.py
     ```

3. **Select OCR Tool**:
   - Choose the OCR tool (e.g., Azure, PaddleOCR, or Tesseract) in the script.

4. **View Output**:
   - The extracted text will be saved in `output.csv`.

---

## Future Enhancements

- Integration with AWS Textract and Google Vision API.
- Improved preprocessing techniques for noisy images.
- Support for multi-language OCR.
- Web-based interface for easier usage.

---

## References

- [Azure Cognitive Services](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/prebuilt/read?view=doc-intel-4.0.0&tabs=sample-code)
- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [AWS Textract](https://aws.amazon.com/textract/)
- [Google Vision API](https://cloud.google.com/vision)