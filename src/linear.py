import json
from typing import Dict, List, Union

import requests
from requests.exceptions import HTTPError
from constants import LINEAR_GRAPHQL_ENDPOINT, LINEAR_TOKEN


def make_linear_call(
    query: str,
) -> Dict[str, Dict[str, Dict[str, List[Dict[str, str]]]]]:
    """
    Function to make a call to linear
    """

    response = requests.post(
        LINEAR_GRAPHQL_ENDPOINT,
        json={"query": query},
        headers={"Authorization": LINEAR_TOKEN},
    )

    if response.status_code != 200:
        raise HTTPError(
            f"Linear API returned status code {response.status_code} with message {response.text}"
        )

    return response.json()


def get_team_list() -> List[Dict[str, Union[str, int]]]:
    """
    Get a list of all teams on linear
    """

    team_list_query = """
        query Teams {
        teams {
            nodes {
            id
            name
            }
        }
        }
        """
    response = make_linear_call(team_list_query)
    values_list = response["data"]["teams"]["nodes"]
    teams_list = [{**value, "value": i} for i, value in enumerate(values_list)]
    return teams_list


def get_project_list() -> List[Dict[str, Union[str, int]]]:
    """
    Get a list of all projects on linear
    """

    project_list_query = """
    query Projects {
    projects(first: 10) {
        nodes {
        id
        name
        state
        teams{
                nodes {
                id
                name
                }
            }
        }
    }
    }
    """

    response = make_linear_call(project_list_query)
    values_list = response["data"]["projects"]["nodes"]
    project_list = [{**value, "value": i} for i, value in enumerate(values_list)]
    return project_list


def get_label_list() -> List[Dict[str, Union[str, int]]]:
    """
    Get a list of all labels on linear
    """

    label_list_query = """
    query issueLabels {
    issueLabels(first: 20) {
        nodes {
        id
        name
        color
        }
    }
    }
    """

    response = make_linear_call(label_list_query)
    values_list = response["data"]["issueLabels"]["nodes"]
    label_list = [{**value, "value": i} for i, value in enumerate(values_list)]
    return label_list


def get_user_list() -> List[Dict[str, Union[str, int]]]:
    """
    Get a list of all users on linear
    """

    user_list_query = """
    query {
        users {
            nodes {
            name
            id
            }
        }
    }
    """

    response = make_linear_call(user_list_query)
    values_list = response["data"]["users"]["nodes"]
    users_list = [{**value, "value": i} for i, value in enumerate(values_list)]
    return users_list


def get_project_issue_list(project_id: str) -> List[Dict[str, str]]:
    """
    Get a list of all issues for a project on linear
    """

    issue_list_query = f"""
    query Issues {{
    issues(projectId: "{project_id}") {{
        nodes {{
        id
        title
        description
        state
        }}
    }}
    }}
    """

    response = make_linear_call(issue_list_query)
    issues_list = response["data"]["issues"]["nodes"]
    return issues_list


def get_user_issue_list(user_id: str) -> List[Dict[str, str]]:
    """
    Get a list of all issues for a user on linear
    """

    issue_list_query = f"""
    query Issues {{
    issues(assigneeId: "{user_id}") {{
        nodes {{
        id
        title
        description
        state
        }}
    }}
    }}
    """
    response = make_linear_call(issue_list_query)
    issues_list = response["data"]["issues"]["nodes"]
    return issues_list


def get_issue_details(issue_id: str) -> List[Dict[str, str]]:
    """
    Get the details of an issue on linear
    """

    issue_details_query = f"""
    query Issue {{
    issue(id: "{issue_id}") {{
        id
        title
        description
        state
        assignee {{
            id
            name
        }}
        project {{
            id
            name
        }}
        team {{
            id
            name
        }}
    }}
    }}
    """
    response = make_linear_call(issue_details_query)
    issue_details = response["data"]["issue"]["nodes"]
    return issue_details


def check_and_extract_team(team_name: str) -> List[Dict[str, str]]:
    """
    Get a list of all teams on linear
    """

    team_list_query = f"""
        query Teams {{
        teams (filter: {{
            name: {{ containsIgnoreCase: "{team_name}" }}
        }}){{
            nodes {{
            id
            name
            }}
        }}
        }}
        """
    response = make_linear_call(team_list_query)

    teams_list = response["data"]["teams"]["nodes"]
    if len(teams_list) == 0:
        raise ValueError("No team found with the given name")
    if len(teams_list) > 1:
        raise ValueError("More than one team found with the given name")
    return teams_list


def check_and_extract_project(project_name: str) -> List[Dict[str, str]]:
    """
    Get a list of all projects on linear
    """

    project_list_query = f"""
    query Projects {{
    projects(filter: {{
      name: {{ containsIgnoreCase: "{project_name}" }}
    }}) {{
        nodes {{
        id
        name
        state
        teams{{
                nodes {{
                id
                name
                }}
            }}
        }}
    }}
    }}
    """

    response = make_linear_call(project_list_query)

    project_list = response["data"]["projects"]["nodes"]
    if len(project_list) == 0:
        raise ValueError("No project found with the given name")
    if len(project_list) > 1:
        raise ValueError("More than one project found with the given name")
    return project_list


def check_and_extract_assignee(assignee_name: str) -> List[Dict[str, str]]:
    user_list_query = f"""
    query {{
            users(filter: {{
            name: {{ containsIgnoreCase: "{assignee_name}" }}
          }}) {{
            nodes {{
            name
            id
            }}
        }}
    }}
    """

    response = make_linear_call(user_list_query)

    users_list = response["data"]["users"]["nodes"]
    if len(users_list) == 0:
        raise ValueError("No user found with the given name")
    if len(users_list) > 1:
        raise ValueError("More than one user found with the given name")
    return users_list


def check_and_extract_labels(labels: List[str]) -> List[List[Dict[str, str]]]:
    label_list: List[List[Dict[str, str]]] = []
    for label in labels:
        label_object = check_and_extract_label(label)
        label_list.append(label_object)
    return label_list


def check_and_extract_label(label: str) -> List[Dict[str, str]]:
    label_list_query = f"""
    query issueLabels {{
    issueLabels(filter: {{
            name: {{ containsIgnoreCase: "{label}" }}
          }}) {{
        nodes {{
        id
        name
        color
        }}
    }}
    }}
    """

    response = make_linear_call(label_list_query)

    label_list = response["data"]["issueLabels"]["nodes"]
    if len(label_list) == 0:
        raise ValueError(f"Label name {label} is invalid")
    return label_list


def create_issue(
    title: str,
    description: str,
    team_id: str,
    project_id: str,
    assignee_id: str,
    label_ids: List[str],
) -> bool:
    """
    Function to create an issue on linear
    """

    input_block = ""

    if title:
        input_block += f"""title: "{title}"\n"""
    if description:
        input_block += f"""description: "{description}"\n"""
    if team_id:
        input_block += f"""teamId: "{team_id}"\n"""
    if project_id:
        input_block += f"""projectId: "{project_id}"\n"""
    if assignee_id:
        input_block += f"""assigneeId: "{assignee_id}"\n"""
    if label_ids:
        input_block += f"""labelIds: {json.dumps(label_ids)}\n"""

    query = f"""
    mutation IssueCreate {{
    issueCreate(
        input: {{
        {input_block}
        }}
    ) {{
        success
        issue {{
        id
        title
        }}
    }}
    }}
    """
    response = make_linear_call(query)
    print(response)
    if response:
        return True
    else:
        return False
