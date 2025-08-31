import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

# usable func
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function

def main():
    load_dotenv()


    print("Hello from agenta!")
    verbose = "--verbose" in sys.argv

    # checking the arguement
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)
    if not args:
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I build a calculator app?"')
        exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    

    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
# AI loop content
    for i in range(20):
        try: 
            response, call_tool = generate_content(client, messages, verbose)
            if response.text and not call_tool:
                print(response.text)
                break
        except Exception as e:
            print("Error when generating content:", e)



def generate_content(client, messages, verbose):
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file
        ]
    )
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """
    model_name = 'gemini-2.0-flash-001'
    response = client.models.generate_content(
        model=model_name,
        contents=messages, 
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        )
    )
    # adding agent's response
    for m in response.candidates:
        messages.append(m.content)

    # 2) collect tool calls from the parts
    answers = []
    call_tool = False
    for cand in response.candidates:
        if not cand or not cand.content:
            continue
        for part in cand.content.parts:
            
            
            if part.function_call:
                call_tool = True
                if verbose:
                    print(f" - Calling function: {part.function_call.name}({part.function_call.args})")
                result = call_function(part.function_call, verbose)
                if (
                    not result.parts
                    or not result.parts[0].function_response
                ):
                    raise Exception("empty function call result")
                answers.append(result.parts[0])
    # if not answers:
    #     raise Exception("no function responses generated, exiting.")
    # 3) if any tool responses, append them as a user message
    if answers:
        messages.append(types.Content(role="user", parts=answers))
    # if call_tool == False:
    #     print("Response:")
    #     print(response.text)
    return response, call_tool


    # if verbose:
    #     print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    #     print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    # if response.function_calls:
    #     answers = []
    #     for function_call_part in response.function_calls:
    #         function_call_result = call_function(function_call_part, verbose)
    #         if (
    #             not function_call_result.parts
    #             or not function_call_result.parts[0].function_response
    #         ):
    #             raise Exception("empty function call result")
    #         if verbose:
    #             print(f"-> {function_call_result.parts[0].function_response.response}")
    #         answers.append(types.Part(function_response=function_call_result.parts[0].function_response))
            

    #         # if function_call_result.parts[0].function_response.response and verbose:
    #         #     print(f"-> {function_call_result.parts[0].function_response.response}")

    #         #     
    #         print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    #     if not answers:
    #         raise Exception("no function responses generated, exiting.")
    #         # else:
    #         #     raise Exception("Fatal") 
    #     print('confirming function response: \n',type(answers[0]), answers[0])
    #     messages.append(types.Content(role='user', parts=answers ))
    # else:
    #     print("Response:")
    #     print(response.text)

    # return response


    ''' solution?
    if not response.function_calls:
        return response.text

    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("empty function call result")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])

    if not function_responses:
        raise Exception("no function responses generated, exiting.")
    '''

if __name__ == "__main__":
    main()
