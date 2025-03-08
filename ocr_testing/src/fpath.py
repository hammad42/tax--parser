import os
from typing import List, Union

def get_file_paths_from_path(input_path: str) -> Union[List[str], None]:
    """
    Retrieves a list of file paths from a given input path, which can be either a file or a folder.

    If the input path is a file, returns a list containing only that file path.
    If the input path is a folder, returns a list containing the paths of all files within that folder.
    If the input path is neither a file nor a folder, prints an error message and returns None.

    Args:
        input_path: The path to a file or folder.

    Returns:
        A list of file paths, or None if the input path is invalid.
    """

    image_paths = []

    if not os.path.exists(input_path):
        print(f"Error: Path does not exist: {input_path}")
        return None

    if os.path.isfile(input_path):
        image_paths = [input_path]
        return image_paths
    elif os.path.isdir(input_path):
        try:
            filenames = os.listdir(input_path)
            for filename in filenames:
                full_path = os.path.join(input_path, filename)
                if os.path.isfile(full_path):
                    image_paths.append(full_path)
            return image_paths
        except OSError as e:
            print(f"Error: Could not read directory {input_path}. {e}")
            return None
    else:
        print(f"Error: Invalid path type: {input_path}. It is neither a file nor a folder.")
        return None