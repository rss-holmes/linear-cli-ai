import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

LINEAR_GRAPHQL_ENDPOINT = os.getenv('LINEAR_GRAPHQL_ENDPOINT')
LINEAR_HEADER_AUTH = os.getenv('LINEAR_HEADER_AUTH')

def make_linear_call(query: str) -> dict or None:
    """
    Function to make a call to linear
    """

    response = requests.post(
        LINEAR_GRAPHQL_ENDPOINT,
        json={"query": query},
        headers={"Authorization": LINEAR_HEADER_AUTH},
    )
    if response.status_code == 200:
        response_json = json.loads(response.text)
        return response_json
    else:
        print(response.json())
        return None


def get_team_list() -> list or None:
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
    if response:
        values_list = response["data"]["teams"]["nodes"]
        teams_list = [{**value, "value": i} for i, value in enumerate(values_list)]
        return teams_list

    return None


def get_project_list() -> list or None:
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
    if response:
        values_list = response["data"]["projects"]["nodes"]
        project_list = [{**value, "value": i} for i, value in enumerate(values_list)]
        return project_list

    return None


def get_label_list() -> list or None:
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
    if response:
        values_list = response["data"]["issueLabels"]["nodes"]
        label_list = [{**value, "value": i} for i, value in enumerate(values_list)]
        return label_list

    return None


def get_user_list() -> list or None:
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
    if response:
        values_list = response["data"]["users"]["nodes"]
        users_list = [{**value, "value": i} for i, value in enumerate(values_list)]
        return users_list

    return None


def get_project_issue_list(self, project_id: str) -> list or None:
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
    response = requests.post(
        self.url, json={"query": issue_list_query}, headers=self.headers
    )
    if response.status_code == 200:
        response_json = json.loads(response.text)
        issues_list = response_json["data"]["issues"]["nodes"]
        return issues_list
    else:
        return None


def get_user_issue_list(self, user_id: str) -> list or None:
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
    response = requests.post(
        self.url, json={"query": issue_list_query}, headers=self.headers
    )
    if response.status_code == 200:
        response_json = json.loads(response.text)
        issues_list = response_json["data"]["issues"]["nodes"]
        return issues_list
    else:
        return None


def get_issue_details(self, issue_id: str) -> dict or None:
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
    response = requests.post(
        self.url, json={"query": issue_details_query}, headers=self.headers
    )
    if response.status_code == 200:
        response_json = json.loads(response.text)
        issue_details = response_json["data"]["issue"]
        return issue_details
    else:
        return None


def create_issue(
    title: str,
    description: str,
    team_id: str,
    project_id: str,
    assignee_id: str,
    label_ids,
) -> None:
    """
    Function to create an issue on linear
    """
    
    query = f"""
    mutation IssueCreate {{
    issueCreate(
        input: {{
        title: "{title}"
        description: "{description}"
        teamId: "{team_id}"
        projectId: "{project_id}"
        assigneeId: "{assignee_id}"
        labelIds: {json.dumps(label_ids)}
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
    # print("issue create")
    # print(response)
    if response:
        return True
    else:
        return False
