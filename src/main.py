import typer
from PyInquirer import Separator, prompt
from rich import print as rprint

from src.linear import (
    create_issue,
    get_label_list,
    get_project_list,
    get_team_list,
    get_user_list,
)

app = typer.Typer()


@app.command("hello")
def sample_func(name: str):
    rprint("[red bold]Hello[/red bold] [yellow]World[yello]")
    module_list_question = [
        {
            "type": "list",
            "name": "username",
            "message": "Select any one username: ",
            "choices": [
                {
                    "name": "Eddie",
                },
                {
                    "name": "Hughie",
                },
                {
                    "name": "Matthew ",
                },
                {
                    "name": "Harvey ",
                },
            ],
        },
        {
            "type": "list",
            "name": "team",
            "message": "Select any one team: ",
            "choices": [
                {
                    "name": "Engineering",
                },
                {
                    "name": "QA",
                },
                {
                    "name": "Product ",
                },
            ],
        },
        {
            "type": "input",
            "name": "commit_name",
            "message": "Give a commit name: ",
        },
        {
            "type": "checkbox",
            "name": "languages",
            "message": "Select the languages: ",
            "choices": [
                {
                    "name": "Python",
                },
                {
                    "name": "Javascript",
                },
                {
                    "name": "Go ",
                },
            ],
        },
        {
            "type": "password",
            "name": "password",
            "message": "Give the password for the operation : ",
        },
        {
            "type": "confirm",
            "name": "confirmation",
            "message": "Confirm all info is fine : ",
        },
    ]

    username = prompt(module_list_question)

    rprint("[yellow]=============================================[yellow]")
    rprint("[green bold]Enter folder name :[green bold]")
    folder_name = input()

    print(f"The username is {username['username']}")
    print(f"The team is {username['team']}")
    print(f"The folder name is {folder_name}")


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


if __name__ == "__main__":
    app()
