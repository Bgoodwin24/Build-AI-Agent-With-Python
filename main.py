import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.call_function import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
args = sys.argv
verbose = "--verbose" in args

if len(args) < 2:
    print("No argument provided, Usage: Name-of-script argument")
    os._exit(1)
elif verbose:
    joined = " ".join([arg for arg in args[1:] if arg != "--verbose"])
else:
    joined = " ".join(args[1:])

user_prompt = joined
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Lists content of files in the specified directory truncated to 10000 characters if exceeding that limit.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to list file contents from, relative to the working directory. If not provided, lists files in the working directory itself."
            ),
        },
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs Python scipt in the specified directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to run Python script from, relative to the working directory. If not provided, lists files in the working directory itself."
            ),
        },
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes files in specified directory. If directory/file doesn't exist it creates the directory first then writes to it",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The directory to write file contents to, relative to the working directory. If not provided, lists files in the working directory itself."
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write into the file/directory, relative to the working directory."
            )
        },
    ),
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
    config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
    )

prompt_token_count = response.usage_metadata.prompt_token_count
candidates_token_count = response.usage_metadata.candidates_token_count
function_call_part = response.function_calls

if function_call_part != []:
    for call in function_call_part:
        function_call_result = call_function(call, verbose=verbose)
        if not hasattr(function_call_result.parts[0], "function_response") or \
        not hasattr(function_call_result.parts[0].function_response, "response"):
            raise Exception("Function call did not produce a function response!")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
else:
    print(response.text)

if verbose:
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {prompt_token_count}")
    print(f"Response tokens: {candidates_token_count}")
