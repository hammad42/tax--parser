import streamlit as st
import src.ocr_selection as ocr
import src.predicted_image as p_image
import src.structured as structured

def main():
    st.title("OCR")

    # Initialize session state
    if "uploaded_files" not in st.session_state:
        st.session_state["uploaded_files"] = None
    if "ocr_results" not in st.session_state:
        st.session_state["ocr_results"] = {}  # Store results per file

    # Step 1: Upload files
    uploaded_files = st.file_uploader("Upload files (or an entire folder)", accept_multiple_files=True)
    if uploaded_files:
        st.session_state["uploaded_files"] = uploaded_files
        st.success(f"Uploaded {len(uploaded_files)} file(s).")
        for file in uploaded_files:
            st.write(f"File: {file.name} - Size: {len(file.getvalue())} bytes")

    # Step 2: OCR processing and editing
    if st.session_state["uploaded_files"]:
        ocr_tool = st.selectbox("Select OCR Tool", ["paddle", "azure"])
        st.write(f"Selected OCR Tool: {ocr_tool}")

        if st.button("Perform OCR"):
            st.session_state["ocr_results"] = {}  # Clear previous results
            for uploaded_file in st.session_state["uploaded_files"]:
                st.write(f"Processing file: {uploaded_file.name} using OCR tool: {ocr_tool}")
                image_bytes = uploaded_file.read()
                results = ocr.perform_ocr(image_bytes, ocr_tool)
                if results:
                    predicted_image = p_image.draw_boxes_on_image(image_bytes, results)
                    st.image(predicted_image, caption=uploaded_file.name, channels="BGR")
                    st.session_state["ocr_results"][uploaded_file.name] = results
                else:
                    st.error(f"An error occurred during OCR processing for {uploaded_file.name}.")

        # Display and edit results
        if st.session_state["ocr_results"]:
            for file_name, results in st.session_state["ocr_results"].items():
                st.subheader(f"Results for {file_name}")
                if results:
                    edited_results = st.data_editor(results, key=f"editor_{file_name}")
                    st.session_state["ocr_results"][file_name] = edited_results
                else:
                    st.write("No OCR results available.")

            if st.button("Save to CSV"):
                all_parsed_data = []
                for file_name, results in st.session_state["ocr_results"].items():
                    if results:
                        parsed_data = structured.parse_ocr_data(results)
                        all_parsed_data.append(parsed_data)

                if all_parsed_data:
                    structured.save_data_to_csv(all_parsed_data)
                    st.success("Data saved to output_ms_ocr.csv")

if __name__ == "__main__":
    main()