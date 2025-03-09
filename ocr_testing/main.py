import streamlit as st
import os
import src.ocr_selection as ocr
import src.predicted_image as p_image

def main():
    st.title("File/Folder Location Fetcher")

    # Initialize session state to store the uploaded files if not already set
    if "uploaded_files" not in st.session_state:
        st.session_state["uploaded_files"] = None

    # Step 1: Upload files (simulating folder upload)
    uploaded_files = st.file_uploader("Upload files (or an entire folder)", accept_multiple_files=True)
    if uploaded_files:
        st.session_state["uploaded_files"] = uploaded_files
        st.success(f"Uploaded {len(uploaded_files)} file(s).")
        # Optionally, you can display file names or additional info
        for file in uploaded_files:
            st.write(f"File: {file.name} - Size: {len(file.getvalue())} bytes")

    # Step 2: Once files are uploaded, allow OCR tool selection and processing
    if st.session_state["uploaded_files"]:
        # Allow the user to select the OCR tool
        ocr_tool = st.selectbox("Select OCR Tool", ["paddle", "azure"])
        st.write(f"Selected OCR Tool: {ocr_tool}")

        # Process the files when the user clicks "Perform OCR"
        if st.button("Perform OCR"):
            for uploaded_file in st.session_state["uploaded_files"]:
                st.write(f"Processing file: {uploaded_file.name} using OCR tool: {ocr_tool}")
                # Read the file as bytes (adjust based on your ocr.perform_ocr implementation)
                image_bytes = uploaded_file.read()
                results = ocr.perform_ocr(image_bytes, ocr_tool)
                if results:
                    # Draw bounding boxes or other annotations on the image using your custom function
                    predicted_image = p_image.draw_boxes_on_image(image_bytes, results)
                    st.image(predicted_image, caption=uploaded_file.name, channels="BGR")
                else:
                    st.error("An error occurred during OCR processing.")

if __name__ == "__main__":
    main()
