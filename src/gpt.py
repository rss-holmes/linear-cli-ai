from typing import Any, Dict, List

import requests

from src.constants import GPT_MODEL, OPENAI_API_KEY
from src.function_schema import functions


def chat_completion_request(
    messages: List[Dict["str", "str"]],
    functions: Any = None,
    model: str = GPT_MODEL,
):
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + OPENAI_API_KEY,
        }
        json_data = {"model": model, "messages": messages, "temperature": 0.0}

        if functions is not None:
            json_data.update({"functions": functions})

        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=json_data,
        )
        return response
    except Exception as err:
        raise ValueError("Unable to generate ChatCompletion response") from err


def setup_ai_system(message_history: List[Dict[str, str]]) -> None:
    system_message = """Don't make assumptions about what values to plug into functions. 
                        Ask for clarification if a user request is ambiguous.
                        If you encounter an error, ask the user for clarification."""
    message_history.append({"role": "system", "content": system_message})


def ask_question(
    message_history: List[Dict["str", "str"]], user_message: str = ""
) -> Dict[str, Dict[str, str]]:
    if not user_message:
        raise ValueError("User message cannot be empty")

    message_history.append({"role": "user", "content": user_message})
    chat_response = chat_completion_request(message_history, functions=functions)
    assistant_message = chat_response.json()["choices"][0]["message"]
    message_history.append(assistant_message)

    return assistant_message
