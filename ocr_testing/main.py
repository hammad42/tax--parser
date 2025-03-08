import streamlit as st
import os
import src.fpath as fp
def main():
    st.title("File/Folder Location Fetcher")

    item_type = st.radio("Select Item Type", ("File", "Folder"))

    if item_type == "File":
        file_path = st.text_input("Enter File Path")
        if file_path:
            if os.path.isfile(file_path):
                st.success(f"File Path: {file_path}")
                st.write(f"File exists.")
                # st.write(f"Absolute Path: {os.path.abspath(file_path)}")
                st.write(f"File Size: {os.path.getsize(file_path)} bytes")
                # st.write(f"Last Modified: {os.path.getmtime(file_path)}")
            image=fp.get_file_paths_from_path(file_path)

            if image:
                st.success(f"Image Path: {image}")

            else:
                st.error("File does not exist or is not a file.")

    elif item_type == "Folder":
        folder_path = st.text_input("Enter Folder Path")
        if folder_path:
            if os.path.isdir(folder_path):
                st.success(f"Folder Path: {folder_path}")
                st.write(f"Folder exists.")
                # st.write(f"Absolute Path: {os.path.abspath(folder_path)}")
                try:
                    files = os.listdir(folder_path)
                    st.write("Files in Folder:")
                    for file in files:
                        st.write(f"- {file}")
                except PermissionError:
                    st.error("Permission denied to access folder contents.")
                except Exception as e:
                    st.error(f"An error occurred: {e}")

            else:
                st.error("Folder does not exist or is not a directory.")

if __name__ == "__main__":
    main()