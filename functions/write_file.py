import os

def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    path = os.path.join(working_directory, file_path)
    target_abs_path = os.path.abspath(path)
    if not target_abs_path.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(target_abs_path):
        try:
            os.makedirs(os.path.dirname(target_abs_path), exist_ok=True)
        except Exception as e:
            return f"Error: creating directory: {e}"
    if os.path.exists(target_abs_path) and os.path.isdir(target_abs_path):
        return f'Error: "{file_path}" is a directory, not a file'
    try:
        with open(target_abs_path, "w") as f:
            f.write(content)
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    except Exception as e:
        return f"Error: writing to file: {e}"
    