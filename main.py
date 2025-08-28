import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

    

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


def main():
    print("Hello from agenta!")
    if len(sys.argv) == 1:
        print("please providing a prompt!")
        exit(1)
    messages = [
        types.Content(role="user", parts=[types.Part(text="user_prompt")]),
    ]
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages 
        # contents=sys.argv[1]
    )
    if "--verbose" in sys.argv:
        print(f"User prompt: {messages}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    

if __name__ == "__main__":
    main()
