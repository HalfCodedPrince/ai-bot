import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types 

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def get_prompt():
    if len(sys.argv) < 2:
        print("Error: No prompt provided")
        sys.exit(1)
    prompt = sys.argv[1]
    parameters = "".join(sys.argv[2:])
    return prompt, parameters

def get_response(user_prompt, messages, parameters="none"):
    response = client.models.generate_content(model="gemini-2.0-flash-001", contents=messages)
    if "--verbose" in parameters:
        prompt_tokens = response.usage_metadata.prompt_token_count
        response_tokens = response.usage_metadata.candidates_token_count
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")
        return response.text
    return response.text

def main():
    user_prompt, parameters = get_prompt()
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]),]
    print(get_response(user_prompt, messages, parameters))

if __name__ == "__main__":
    main()
