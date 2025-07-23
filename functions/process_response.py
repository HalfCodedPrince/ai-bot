from google.genai import types 

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
    
    # start constructing the output with the function_calls (if there are function.calls):
    if response.function_calls:
        for function in response.function_calls:
            entire_response.append(f"Calling function: {function.name}({function.args})")

    # add .text if it's not None:
    if response.text:
        entire_response.append(response.text)
    
    # ignore the SDK telling you there are non-text parts
    return "\n".join(entire_response)

