import json
from typing import Dict, List, cast

import typer
from PyInquirer import prompt  # type: ignore
from rich import print as rprint

from configure import configure_system
from gpt import ask_question, setup_ai_system
from linear import (
    create_issue,
    get_label_list,
    get_project_list,
    get_team_list,
    get_user_list,
)
from linear_ai import create_issue_ai, get_team_list_ai

app = typer.Typer()


@app.command("configure")
def configure():
    gpt_models_list = [
        {
            "name": "gpt-3.5-turbo-0613",
        },
        {
            "name": "gpt4",
        },
    ]

    rprint("[yellow]Provide the following details : [yellow]")

    config_input_list: List[Dict[str, str]] = [
        {
            "type": "input",
            "name": "linear_api_token",
            "message": "Linear API Token : ",
        },
        {
            "type": "input",
            "name": "openai_api_key",
            "message": "OpenAI API Key : ",
        },
        {
            "type": "list",
            "name": "gpt_model",
            "message": "Select the model you will use : ",
            "choices": gpt_models_list,
        },
    ]

    config_data = cast(Dict[str, str], prompt(config_input_list))

    linear_api_token: str = config_data["linear_api_token"]
    openai_api_key: str = config_data["openai_api_key"]
    gpt_model: str = config_data["gpt_model"]

    configure_system(linear_api_token, openai_api_key, gpt_model)


@app.command("create-issue")
def create_issue_interface():
    rprint("[yellow]Provide the following details : [yellow]")

    team_list = get_team_list()
    user_list = get_user_list()
    project_list = get_project_list()
    label_list = get_label_list()
    issue_creation_input_list = [
        {
            "type": "input",
            "name": "title",
            "message": "Title of the issue : ",
        },
        {
            "type": "input",
            "name": "description",
            "message": "Description for the issue : ",
        },
        {
            "type": "list",
            "name": "team",
            "message": "Select a team for the issue : ",
            "choices": team_list,
        },
        {
            "type": "list",
            "name": "assignee",
            "message": "Select an assignee for the issue : ",
            "choices": user_list,
        },
        {
            "type": "list",
            "name": "project",
            "message": "Select a project for the issue : ",
            "choices": project_list,
        },
        {
            "type": "checkbox",
            "name": "labels",
            "message": "Select the labels for the issue : ",
            "choices": label_list,
        },
    ]

    issue_data = prompt(issue_creation_input_list)

    title = issue_data["title"]
    description = issue_data["description"]
    team_id = issue_data["team"]
    assignee_id = issue_data["assignee"]
    project_id = issue_data["project"]
    labels = issue_data["labels"]

    rprint("[yellow]=============================================[yellow]")
    rprint("[green bold]Issue Creation Details :[green bold]")
    rprint(f"[green bold]Title :[green bold] {title}")
    rprint(f"[green bold]Description :[green bold] {description}")
    rprint(f"[green bold]Team :[green bold] {team_list[team_id]['name'] }")
    rprint(f"[green bold]Assignee :[green bold] {user_list[assignee_id]['name'] }")
    rprint(f"[green bold]Project :[green bold] {project_list[project_id]['name'] }")
    rprint(
        f"[green bold]Labels :[green bold] {[label_list[label]['name'] for label in labels]}"
    )

    issue_confirmation_list = [
        {
            "type": "confirm",
            "name": "confirmation",
            "message": "Confirm that the data is correct : ",
        },
    ]

    confirmation_data = prompt(issue_confirmation_list)

    if confirmation_data["confirmation"]:
        rprint("[green bold]Creating the issue ... [green bold]")
        issue_created = create_issue(
            title,
            description,
            team_list[team_id]["id"],
            project_list[project_id]["id"],
            user_list[assignee_id]["id"],
            [label_list[label]["id"] for label in labels],
        )
        if issue_created:
            rprint("[green bold]Issue created successfully [green bold]")
        else:
            rprint("[red bold]Error while creating the issue [red bold]")
    else:
        rprint("[red bold]Issue creation cancelled. [red bold]")


@app.command("create-issue-ai")
def create_issue_ai_interface():
    running = 1
    message_history: List[Dict[str, str]] = []
    setup_ai_system(message_history)
    user_message = input("What would you like to do on linear : ")

    while running:
        try:
            assistant_msg = ask_question(message_history, user_message)

            if "function_call" in assistant_msg:
                function_name = assistant_msg["function_call"]["name"]
                function_args = assistant_msg["function_call"]["arguments"]

                if function_name == "create_issue":
                    create_issue_ai(**json.loads(function_args))
                elif function_name == "get_team_list":
                    get_team_list_ai(**json.loads(function_args))

                running = 0
            else:
                # gpt couldn't come up with a function call and needs more input
                print(f"\n {assistant_msg['content']}")
                input_message = input("Enter a message: ")
                user_message = f"Use '{input_message}' to correct the previous error and create the issue"
        except Exception as e:
            print("There was an error while calling function")
            print(e)
            user_message = (
                f"""Encountered an error during creating issue. Error is {e}"""
            )


if __name__ == "__main__":
    app()
