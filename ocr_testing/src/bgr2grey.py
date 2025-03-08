import cv2
import os

def convert_to_grayscale(image_path_or_folder, output_folder="gray_images"):
    """
    Converts an image or a batch of images in a folder to grayscale.

    Args:
        image_path_or_folder: Path to a single image or a folder containing images.
        output_folder: Path to the output folder. Defaults to "gray_images".

    Returns:
        A list of paths to the saved grayscale images, or None if an error occurred.
        If a single image is processed, returns a list containing one path.
    """

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    saved_paths = []

    if os.path.isfile(image_path_or_folder):  # Process a single image
        image_paths = [image_path_or_folder]  # Make it a list for consistent processing
    elif os.path.isdir(image_path_or_folder):  # Process a folder of images
        image_paths = [
            os.path.join(image_path_or_folder, filename)
            for filename in os.listdir(image_path_or_folder)
            if os.path.isfile(os.path.join(image_path_or_folder, filename)) # Check if it is a file
        ]
    else:
        print(f"Error: Invalid path: {image_path_or_folder}")
        return None

    for image_path in image_paths:
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error: Could not read image at {image_path}")
            continue  # Skip to the next image

        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image_name = os.path.basename(image_path)
        gray_image_name = "gray_" + image_name
        gray_image_path = os.path.join(output_folder, gray_image_name)

        cv2.imwrite(gray_image_path, gray_image)
        print(f"Grayscale image saved to {gray_image_path}")
        saved_paths.append(gray_image_path)

    return saved_paths


if __name__ == "__main__":
    # Example 1: Processing a single image
    # single_image_path = r"E:\Projects\OCR\ocr_testing\test.jpg"  # Replace with your image path
    # gray_paths = convert_to_grayscale(single_image_path)
    # if gray_paths:
    #     print("Grayscale images saved:", gray_paths)

    # Example 2: Processing a folder of images
    folder_path = r"samples\color_smples"  # Replace with your folder path
    gray_paths = convert_to_grayscale(folder_path, output_folder="samples\gray_images") # Specify a different output folder
    if gray_paths:
        print("Grayscale images saved:", gray_paths)


    # # Example 3: Invalid path
    # invalid_path = "non_existent_path"
    # gray_paths = convert_to_grayscale(invalid_path)
    # if gray_paths is None:
    #     print("Grayscale conversion failed.")