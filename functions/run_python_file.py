import os, subprocess

def run_python_file(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    path = os.path.join(working_directory, file_path)
    target_abs_path = os.path.abspath(path)
    if not target_abs_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(target_abs_path):
        return f'Error: File "{file_path}" not found.'
    if not target_abs_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        run = subprocess.run(["python3", file_path], timeout=30, capture_output=True, cwd=working_directory)
        stdout = run.stdout.decode().strip()
        stderr = run.stderr.decode().strip()
        if len(stdout) == 0 and len(stderr) == 0:
            return "No output produced."
        result = f'STDOUT: {stdout}\nSTDERR: {stderr}'
        if run.returncode != 0:
            result += " " + f'Process exited with code {run.returncode}'
        return result.strip()
    except Exception as e:
        return f'Error: executing Python file: {e}'
    