import os
from google.genai import types 

def write_file(working_directory, file_path, content):
    absolute_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    absolute_working_dir_path = os.path.abspath(working_directory)
    # in case an empty string is passed, it will be checked later with -if.
    parent_dir = os.path.dirname(absolute_file_path)


    try:
        if os.path.commonpath([absolute_working_dir_path, absolute_file_path]) != absolute_working_dir_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    # the -if check
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)

        with open(absolute_file_path, "w") as file:
            file.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'


    except Exception as e:
        return f"Error: {e}"
    

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