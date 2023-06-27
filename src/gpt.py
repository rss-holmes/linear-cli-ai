import json
import os
import requests
from dotenv import load_dotenv

from function_schema import functions
from linear_ai import create_issue_ai

load_dotenv()

GPT_MODEL = os.getenv("GPT_MODEL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def chat_completion_request(
    messages, functions=None, function_call=None, model=GPT_MODEL
):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + OPENAI_API_KEY,
    }
    json_data = {"model": model, "messages": messages, "temperature": 0.0}

    if functions is not None:
        json_data.update({"functions": functions})

    if function_call is not None:
        json_data.update({"function_call": function_call})
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=json_data,
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e


def setup_ai_system(message_history):
    system_message = """Don't make assumptions about what values to plug into functions. 
                        Ask for clarification if a user request is ambiguous."""
    message_history.append({"role": "system", "content": system_message})


def ask_question(message_history, user_message=''):
    if not user_message:
        return
    message_history.append({"role": "user", "content": user_message})
    print(f"User Message: {user_message}")
    chat_response = chat_completion_request(message_history, functions=functions)
    assistant_message = chat_response.json()["choices"][0]["message"]
    print(f"Assistant Message: {assistant_message}")
    message_history.append(assistant_message)

    return assistant_message

if __name__ == "__main__":
    running  = 1
    user_message = input("What would you like to do on linear : ")
    # user_message = """Create an issue with description 'Rewrite the print service with queue system'
    #                   and title as 'Print Service v2.0' and team as 'engineering' and assign it to 'Rohan' 
    #                   and add labels 'bug' and 'high priority' and add it to project 'Print Service'"""
    message_history = []
    setup_ai_system(message_history)
    while running:
        try:
            message = ask_question(message_history, user_message)
            if 'function_call' in message:
                function_call = message['function_call']
                if function_call['name'] == 'create_issue':
                    create_issue_ai(**json.loads(function_call['arguments']))
                    running = 0
            else:
                print("\n")
                print(message["content"])
                input_message = input("Enter a message: ")
                user_message = f"Use '{input_message}' to correct the previous error and create the issue"
        except Exception as e:
            print("Error in linear cli : ")
            print(e)
            user_message = f"""Encountered an error during creating issue. Error is {e}"""



