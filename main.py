import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types 
from functions.get_files_info import schema_get_files_info
from functions.process_response import process_response

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# messages - message history, so far kept in RAM. 
# system promt is a roleplay paramater for GenerateContentConfig
# available functions - schemas for the LLM, basically telling it "here's a thing you can use" 
messages = []
system_promt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
available_functions = types.Tool(function_declarations=[schema_get_files_info,])


def get_prompt():
    if len(sys.argv) < 2:
        print("Error: No prompt provided")
        sys.exit(1)
    prompt = sys.argv[1]
    parameters = "".join(sys.argv[2:])
    return prompt, parameters


# see functions/process_response.py for the response formatting
def get_response(user_prompt, messages, parameters="none"):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents=messages, 
        config=types.GenerateContentConfig(system_instruction=system_promt, tools = [available_functions]))
    
    return process_response(user_prompt, response, parameters)  

def main():
    user_prompt, parameters = get_prompt()
    messages.append(types.Content(role="user", parts=[types.Part(text=user_prompt)]))
    print(get_response(user_prompt, messages, parameters))

if __name__ == "__main__":
    main()
