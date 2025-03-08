import streamlit as st
import os
import src.fpath as fp
import src.ocr_selection as ocr
import src.predicted_image as p_image
def main():
    st.title("File/Folder Location Fetcher")




    # Ensure session state key exists for images
    if "images" not in st.session_state:
        st.session_state["images"] = None

    # Step 1: Input the file path and submit
    file_path = st.text_input("Enter File Path")
    if st.button("Submit"):
        images = fp.get_file_paths_from_path(file_path)
        if isinstance(images, list):
            st.session_state["images"] = images  # Save the image list in session state
            st.success("File(s) loaded successfully!")
            st.write(f"Number of Files: {len(images)}")
            st.write(f"File Size: {os.path.getsize(file_path)} bytes")
        else:
            st.error("Error: " + str(images))

    # Step 2: If file paths are loaded, allow OCR tool selection and OCR processing
    if st.session_state["images"]:
        # Allow user to select the OCR tool
        ocr_tool = st.selectbox("Select OCR Tool", ["paddle", "azure"])
        st.write(f"Selected OCR Tool: {ocr_tool}")
        
        # Wait for the user to click "Perform OCR" to start processing
        if st.button("Perform OCR"):
            for image in st.session_state["images"]:
                st.write(f"Processing image: {image} using OCR tool: {ocr_tool}")
                results = ocr.perform_ocr(image, ocr_tool)
                if results:
                    print(results)
                    predicted_image=p_image.draw_boxes_on_image(image,results)
                    st.image(predicted_image, channels="BGR", caption=image)
                    # for item in results:
                    #     st.write(f"Text: {item['text']}")
                    #     st.write(f"Bounding Box: {item['bounding_box']}")
                    #     st.write(f"Confidence: {item['confidence']}")
                else:
                    st.error("An error occurred during OCR processing.")


if __name__ == "__main__":
    main()