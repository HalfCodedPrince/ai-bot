from google.genai import types
from config import WORKING_DIR
from tools import FUNCTION_DICT

from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file


# interpeter for actually calling the specified function and then returning the result back to LLM

def call_function(function_call_part, verbose=False):
    function_called_str = function_call_part.name
    # a dict copy just in case, will add logic for it config later
    args_dict = function_call_part.args.copy()

    # simply add the working directory to the dict, since I'm unpacking it anyway. 
    args_dict["working_directory"] = WORKING_DIR

    # current functions for LLM to call, stored in the dict in root/tools.py
    current_func_dict = FUNCTION_DICT
    
    selected_function = current_func_dict.get(function_called_str)

    # check for --verbose flag
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    

    # check if the function called actually exists
    if selected_function == None:
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_called_str,
                        response={"error": f"Unknown function: {function_called_str}"},
                        )
                    ],
                )
    
    # try to run the function; if everything is on fire, tell the LLM
    try:
        return types.Content(
                role="tool",
                parts=[
                        types.Part.from_function_response(
                            name=function_called_str,
                            response={"result": selected_function(**args_dict)},
                            )
                    ],
                )
       
    except Exception as e:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_called_str,
                    response={"error": f"{e}"},
                    )
                ],
            )