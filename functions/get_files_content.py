import os

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
