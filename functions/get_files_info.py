import os 

from google.genai import types


def get_files_info(working_directory, directory="."):
    
    # Railguard for path 
    abs_ori = os.path.abspath(working_directory)
    abs_pass = os.path.abspath(os.path.join(working_directory, directory))
    if not abs_pass.startswith(abs_ori):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(abs_pass):
        return f'Error: "{directory}" is not a directory'

    try:
        res = []
        for fil in os.listdir(abs_pass):
            dire = os.path.join(abs_pass,  fil)
            res.append(f"- {fil}: file_size={os.path.getsize(dire)} bytes, is_dir={os.path.isdir(dire)}")
        return "\n".join(res)
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