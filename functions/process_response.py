from google.genai import types 
from functions.call_function import call_function

# Gemini seems to return "None" in response.text or function_calls and then everything is on fire if I try to do it easier.
# Hence, variable handling (until I have/need a better way)

def process_response(user_prompt, response, parameters):
    entire_response = []

    if "--verbose" in parameters:
        prompt_tokens = response.usage_metadata.prompt_token_count
        response_tokens = response.usage_metadata.candidates_token_count
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")
    
    # start constructing the output with the [function_calls] (if there are [function.calls]):
    if response.function_calls:
        for function in response.function_calls:
            # if we have any functions, actually process them (see call_function.py)
            
            # "--verbose" in parameters equal either True or False, sending it back as a bool
            function_call_result = call_function(function, "--verbose" in parameters)
            # check if the return parts object a) exists and b) has the correct value in index [0] (or if everything is on fire)
            if not function_call_result.parts or not hasattr(function_call_result.parts[0], "function_response"):
                raise RuntimeError("Function did not return function_response in parts!")
            
            if "--verbose" in parameters:
                print(f"-> {function_call_result.parts[0].function_response.response}")
            # okay, here's the thing: parts[0] exsists and I checked that it's a function_response-object-thingy. 
            # So we access it's response value, because the response syntax is zogging bootiful:
            entire_response.append(str(function_call_result.parts[0].function_response.response))

    # add .text if it's not None:
    if response.text:
        entire_response.append(response.text)
    
    # ignore the SDK telling you there are non-text parts, because usually it's either .text or [function_calls]
    return "\n".join(entire_response)

