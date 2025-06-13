import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)
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
content = client.models.generate_content(model="gemini-2.0-flash-001", contents=messages)

prompt_token_count = content.usage_metadata.prompt_token_count
candidates_token_count = content.usage_metadata.candidates_token_count

print(content.text)

if verbose:
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {prompt_token_count}")
    print(f"Response tokens: {candidates_token_count}")
