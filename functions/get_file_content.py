import os
from google.genai import types 

MAX_CHARS = 10000

def get_file_content(working_directory, file_path):
    absolute_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    absolute_working_dir_path = os.path.abspath(working_directory)

    try:
        if os.path.commonpath([absolute_working_dir_path, absolute_file_path]) != absolute_working_dir_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        elif not os.path.isfile(absolute_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        else:
            try:
                with open(absolute_file_path, "r") as file:
                    have_read_file = file.read(MAX_CHARS + 1)
                    if len(have_read_file) > MAX_CHARS:
                        return have_read_file[:MAX_CHARS] + f'[...File "{file_path}" truncated at 10000 characters]'
                    return have_read_file
            except Exception as e:
                return f"Error: {e}"

    except Exception as e:
        return f"Error: {e}"

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