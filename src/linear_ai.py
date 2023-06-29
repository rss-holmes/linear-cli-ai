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
    # print("Validating the inputs")
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
        # print(team_object)
        team_id = team_object[0]["id"]

    project_object = []
    project_id: str = ""
    if project_name:
        project_object = check_and_extract_project(project_name)
        # print(project_object)
        project_id = project_object[0]["id"]

    assignee_id: str = ""
    assignee_object = []
    if assignee_name:
        assignee_object = check_and_extract_assignee(assignee_name)
        # print(assignee_object)
        assignee_id = assignee_object[0]["id"]

    label_objects = []
    label_ids: Set[str] = set()
    label_names: Set[str] = set()
    if labels:
        label_objects = check_and_extract_labels(labels)
        # print(label_objects)
        for label_lists in label_objects:
            for label in label_lists:
                label_ids.add(label["id"])
                label_names.add(label["name"])

    final_message = "Creating issue with the given inputs: \n"

    if title:
        final_message += f"""Title : "{title}"\n"""
    if description:
        final_message += f"""Description : "{description}"\n"""
    if team_object:
        final_message += f"""Team : "{team_object[0]['name']}"\n"""
    if project_object:
        final_message += f"""projectId: "{project_object[0]['name']}"\n"""
    if assignee_object:
        final_message += f"""assigneeId: "{assignee_object[0]['name']}"\n"""
    if label_ids:
        final_message += f"""labelIds: {list(label_names)}\n"""

    return_dict = {
        "message": final_message,
        "data": {
            "title": title,
            "description": description,
            "team_id": team_id,
            "project_id": project_id,
            "assignee_id": assignee_id,
            "label_ids": list(label_ids),
        },
    }

    return return_dict


def get_team_list_ai(
    team_name: str = "",
):
    pass
