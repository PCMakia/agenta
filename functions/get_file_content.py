import os 
from config import CHARACTER_LIMIT

def get_file_content(working_directory, file_path):
    # Railguard for path 
    abs_ori = os.path.abspath(working_directory)
    abs_pass = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_pass.startswith(abs_ori):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_pass):
        return f'Error: File not found or is not a regular file: "{file_path}"'


    try:
        # open file
        with open(abs_pass, "r") as f: 
            file_content_string = f.read(CHARACTER_LIMIT)

        if os.path.getsize(abs_pass) > CHARACTER_LIMIT:
            file_content_string += f'[...File "{file_path}" truncated at {CHARACTER_LIMIT} characters]'
        return file_content_string
    except Exception as e:
        return f"Error: {e}"