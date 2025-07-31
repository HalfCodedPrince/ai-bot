import os
import sys
import pprint

from dotenv import load_dotenv
from google import genai
from google.genai import types

from config import MAX_ITER, SYSTEM_PROMPT
from tools import SCHEMA_LIST

from functions.call_function import call_function
from functions.process_response import process_response

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# messages - message history, so far kept in RAM. 
messages = []

# max_iterations - how many times feedback loop will run until either stopping or returning an answer
# system promt is a roleplay paramater for GenerateContentConfig
# available functions - schemas for the LLM, basically telling it "here's a thing you can use" 
max_iterations = MAX_ITER
system_promt = SYSTEM_PROMPT 
available_functions = types.Tool(function_declarations=SCHEMA_LIST)


def get_prompt():
    if len(sys.argv) < 2:
        print("Error: No prompt provided")
        sys.exit(1)
    prompt = sys.argv[1]
    parameters = "".join(sys.argv[2:])
    return prompt, parameters


def get_response(user_prompt, messages, parameters="none"):
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-001", 
            contents=messages, 
            config=types.GenerateContentConfig(system_instruction=system_promt, tools = [available_functions]))
    except Exception as e:
        # GEMINI seems to be overloaded quite often
        print(f"Error during LLM content generation: {e}.")
        sys.exit(1)
    
    # see functions/process_response.py for user response formatting
    display_to_user_str = process_response(user_prompt, response, parameters)

    # response object itself is sent for building feedback look
    return display_to_user_str, response


def create_feedback_loop(response):
    # okay, first it goes through the candidates object and adds them to [messages]
    if response.candidates:
        for candidate_answer in response.candidates:
            if candidate_answer.content:
                messages.append(candidate_answer.content)
    
    # Then, pretending there ain't no "D" in "DRY", repeat a slitghly changed bit from process_response
    # Check if there were function calls; if there were, return the types.content object for each function via functions/call_function.py (return is already formatted correctly)
    if response.function_calls and hasattr(response, "function_response"):
        for function in response.function_calls:
            function_call_result = call_function(function)
            messages.append(function_call_result)



def main():
    user_prompt, parameters = get_prompt()
    messages.append(types.Content(role="user", parts=[types.Part(text=user_prompt)]))

    # iterate max_iterations times (so the LLM would actually stop at some point, if there are issues)
    for _ in range(max_iterations):
        response_to_user, response = get_response(user_prompt, messages, parameters)
        create_feedback_loop(response)
        
        # if you need to check the "thinking" proccess - uncomment this:
        print("\n=== Messages so far ===\n")
        for i, msg in enumerate(messages):
            print(f"Message {i}:")
            pprint.pprint({
                "role": msg.role,
                "parts": [part.text if hasattr(part, "text") else str(part) for part in msg.parts]
            })
            print("-----")

        # if this is REALLY the actual answer, then please, return it to user
        if not getattr(response, "function_calls", None) and response.text:
            print(response_to_user)
            break
 


if __name__ == "__main__":
    main()
