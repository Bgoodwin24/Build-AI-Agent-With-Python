import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    path = os.path.join(working_directory, file_path)
    target_abs_path = os.path.abspath(path)
    if not target_abs_path.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if os.path.isfile(path) == False:
        return f'Error: File not found or is not a regular file: "{file_path}"'


    try:
        with open(path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if f.read(1):
                return f'{file_content_string} [...File "{file_path}" truncated at 10000 characters]'
            else:
                return file_content_string
    except Exception as e:
        return f'Error: {e}'
