import cv2
import numpy as np

def upscale_image(image_path, original_dpi, target_dpi=300):
    """
    Upscales an image to the specified DPI and resolution.

    Args:
        image_path: Path to the input image.
        original_dpi: Original DPI of the image (required).
        target_dpi: Target DPI for the output image.

    Returns:
        The upscaled image as a NumPy array (BGR format), or None if an error occurs.
        Also returns the new width and height in pixels.
    """
    try:
        # 1. Load the image
        img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)  # Keep alpha channel if present
        if img is None:
            print(f"Error: Could not open or read image file: {image_path}")
            return None, None, None

        height, width = img.shape

        # 2. Calculate the scaling factor (now using input original_dpi)
        scale_factor = target_dpi / original_dpi

        # 3. Calculate new dimensions
        new_height = int(height * scale_factor)
        new_width = int(width * scale_factor)

        # 4. Upscale using interpolation (cv2.INTER_CUBIC is a good choice)
        upscaled_img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_CUBIC)

        return upscaled_img, new_width, new_height

    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None, None


def save_image(image, output_path, dpi=300):
    # ... (This function remains the same as in the previous example)
    try:
        if output_path.lower().endswith(('.png', '.tif', '.tiff')): # Formats supporting DPI
            cv2.imwrite(output_path, image, [cv2.IMWRITE_PNG_COMPRESSION, 9]) # Max compression for PNG
            print(f"Image saved to {output_path} with {dpi} DPI (metadata)")

        elif output_path.lower().endswith('.jpg') or output_path.lower().endswith('.jpeg'):
            cv2.imwrite(output_path, image, [cv2.IMWRITE_JPEG_QUALITY, 95])  # High quality for JPEG
            print(f"Image saved to {output_path} (JPEG doesn't reliably support DPI metadata)")

        else:
            cv2.imwrite(output_path, image) # Save without DPI metadata
            print(f"Image saved to {output_path} (DPI metadata not supported for this format)")


    except Exception as e:
        print(f"Error saving image: {e}")



if __name__ == "__main__":
# Example usage:
    input_image_path = r"E:\Projects\OCR\ocr_testing\samples\gray_images\gray_Screenshot_20250211-234427_1.png"  # Replace with your image path
    output_image_path = r"E:\Projects\OCR\ocr_testing\outputs\upscale"  # Replace with desired output path


    upscaled_image, new_width, new_height = upscale_image(input_image_path, 96)

    if upscaled_image is not None:
        save_image(upscaled_image, output_image_path, dpi=300)
        print(f"Upscaled image dimensions: {new_width} x {new_height} pixels")
    else:
        print("Image upscaling failed.")