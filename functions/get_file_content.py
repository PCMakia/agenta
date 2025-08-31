import os 
from config import CHARACTER_LIMIT
from google.genai import types

def get_file_content(working_directory, file_path):
    # Railguard for path 
    if file_path.startswith("calculator/"): 
        file_path = file_path.split("calculator/", 1)[1]
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

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Reads and returns the first {CHARACTER_LIMIT} characters of the content from a specified file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file whose content should be read, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)
