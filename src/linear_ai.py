from typing import Dict, List
from linear import (
    check_and_extract_assignee,
    check_and_extract_labels,
    check_and_extract_project,
    check_and_extract_team,
)


def create_issue_ai(
    title: str,
    description: str,
    project_name: str = "",
    assignee_name: str = "",
    labels: List[str] = list(),
    team_name: str = "",
):
    print("Validating the inputs")
    if not title:
        raise ValueError("Title cannot be empty")

    if not description:
        raise ValueError("Title cannot be empty")

    team_object = []
    if team_name:
        team_object = check_and_extract_team(team_name)
        print(team_object)

    project_object = []
    if project_name:
        project_object = check_and_extract_project(project_name)
        print(project_object)

    assignee_object = []
    if assignee_name:
        assignee_object = check_and_extract_assignee(assignee_name)
        print(assignee_object)

    label_objects = []
    if labels:
        label_objects = check_and_extract_labels(labels)
        print(label_objects)

    create_issue_with_valid_inputs(
        title, description, team_object, project_object, assignee_object, label_objects
    )


def create_issue_with_valid_inputs(
    title: str,
    description: str,
    team_object: List[Dict[str, str]],
    project_object: List[Dict[str, str]],
    assignee_object: List[Dict[str, str]],
    label_objects: List[List[Dict[str, str]]],
):
    print("Creating issue with the given inputs \n")

    print(f"The title is {title}")
    print(f"The description is {description}")
    print(f"The team is {team_object}")
    print(f"The project is {project_object}")
    print(f"The assignee is {assignee_object}")
    print(f"The labels are {label_objects}")


def get_team_list_ai(team_name: str = "",):
    pass