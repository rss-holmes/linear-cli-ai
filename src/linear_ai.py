from typing import List, Set

from src.linear import (
    check_and_extract_assignee,
    check_and_extract_labels,
    check_and_extract_project,
    check_and_extract_team,
    create_issue,
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

    if not team_name:
        raise ValueError("Team Name cannot be empty")

    team_object = []
    team_id: str = ""
    if team_name:
        team_object = check_and_extract_team(team_name)
        print(team_object)
        team_id = team_object[0]["id"]

    project_object = []
    project_id: str = ""
    if project_name:
        project_object = check_and_extract_project(project_name)
        print(project_object)
        project_id = project_object[0]["id"]

    assignee_id: str = ""
    assignee_object = []
    if assignee_name:
        assignee_object = check_and_extract_assignee(assignee_name)
        print(assignee_object)
        assignee_id = assignee_object[0]["id"]

    label_objects = []
    label_ids: Set[str] = set()
    if labels:
        label_objects = check_and_extract_labels(labels)
        print(label_objects)
        label_ids: Set[str] = set()
        for label_lists in label_objects:
            for label in label_lists:
                label_ids.add(label["id"])

    print(
        f"""Creating issue with the given inputs: \n
        Title : {title}\n 
        Description : {description}\n 
        Team : {team_object}\n 
        Project : {project_object}\n 
        Assignee : {assignee_object}\n 
        Labels : {label_objects}\n"""
    )

    create_issue(title, description, team_id, project_id, assignee_id, list(label_ids))


def get_team_list_ai(
    team_name: str = "",
):
    pass
