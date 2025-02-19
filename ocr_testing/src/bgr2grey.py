import cv2
import os

def convert_to_grayscale(image_path, output_folder="gray_images"):
    """
    Converts an image to grayscale and saves it to a specified output folder.

    Args:
        image_path: Path to the input image.
        output_folder: Path to the output folder where the grayscale image 
                       will be saved. Defaults to "gray_images" in the 
                       same directory as the script.
    
    Returns:
        The path to the saved grayscale image, or None if an error occurred.
    """

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Could not read the image at {image_path}. Check the file path.")
        return None

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Extract the image filename from the input path
    image_name = os.path.basename(image_path)
    gray_image_name = "gray_" + image_name  # Or just image_name if you want to overwrite
    gray_image_path = os.path.join(output_folder, gray_image_name)

    cv2.imwrite(gray_image_path, gray_image)
    print(f"Grayscale image saved to {gray_image_path}")
    return gray_image_path

if __name__ == "__main__":
    image_path = r"E:\Projects\OCR\ocr_testing\test.jpg"
    convert_to_grayscale(image_path)