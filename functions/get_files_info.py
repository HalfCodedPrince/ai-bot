import os
from google import genai
from google.genai import types

def get_files_info(working_directory, directory="."):
    absolute_dir_path = os.path.abspath(os.path.join(working_directory, directory))
    absolute_working_dir_path = os.path.abspath(working_directory)

    # all errors should be returned as strings, so try/except:
    try:
        if not os.path.isdir(absolute_dir_path):
            return f'Error: "{directory}" is not a directory'
        elif os.path.commonpath([absolute_working_dir_path, absolute_dir_path]) == absolute_working_dir_path:
            contents = os.listdir(absolute_dir_path)
            formatted_contents = []
            for file in contents:
                path_to = os.path.join(absolute_dir_path, file)
                formatted_file_str = f'- {file}: file_size={os.path.getsize(path_to)} bytes, is_dir={os.path.isdir(path_to)}'
                formatted_contents.append(formatted_file_str)
            return "\n".join(formatted_contents)

        else:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
    except Exception as e:
        return f"Error: {e}"
    
    
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
