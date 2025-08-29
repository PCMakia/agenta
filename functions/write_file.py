import os 

def write_file(working_directory, file_path, content):
    # Railguard for path 
    abs_ori = os.path.abspath(working_directory)
    abs_pass = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_pass.startswith(abs_ori):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    # if not os.path.exists(abs_pass):
    #     os.makedirs(abs_pass)
    
    try:
        with open(abs_pass, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"    
        