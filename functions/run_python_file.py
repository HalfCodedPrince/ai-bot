import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    absolute_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    absolute_working_dir_path = os.path.abspath(working_directory)
    
    try:
        if os.path.commonpath([absolute_working_dir_path, absolute_file_path]) != absolute_working_dir_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        elif not os.path.isfile(absolute_file_path):
            return f'Error: File "{file_path}" not found.'       
        elif not absolute_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        # running a python file with args 
        # -- inside the working directory, timeout = 30 sec, stderr and stdout is captured in a string
        try:
            run_file = subprocess.run(["python", f"{absolute_file_path}"] + args, cwd=absolute_working_dir_path, capture_output=True, text=True, timeout=30)
            result = f"STDOUT: {run_file.stdout}, STDERR:{run_file.stderr}"
            if run_file.returncode != 0:
                result += f" Process exited with code {run_file.returncode}"
        
            if not run_file.stdout and not run_file.stderr and run_file.returncode == 0:
                return "No output produced"
            
            return result
        
        except Exception as e:
            return f"Error: executing Python file: {e}"


    except Exception as e:
        return f"Error: {e}"