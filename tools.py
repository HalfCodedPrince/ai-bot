from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

# current functions
FUNCTION_DICT = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file,
        }

# current schemas (see SCHEMA_LIST at the bottom). Might need its own file at some point, but should be good for now
schema_get_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Opens and reads a file based on the file path provided. If the number of characters in the file is more than 10 000, the functions returns only the first 10 000.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file the functions intends to open",
            ),
        },
    ),
)


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


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file (.py) with arguments provided by the args parameters. The path to the file is determined by file_path argument",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file the function intends to open",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING
                ),
                description="Optional arguments. The list of command-line arguments passed to the pyton file in the file_path. Each list item is a separate argument represented by a string"
            )
        },
    ),
)
    

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the provided content-argument into the file. The path to the file used determined by the file_path-argument",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file the functions intends to write to",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The string function writes into the file"
            )
        },
    ),
)


SCHEMA_LIST = [schema_get_files_info, schema_get_content, schema_run_python_file, schema_write_file]