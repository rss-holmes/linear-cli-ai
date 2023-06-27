from linear import make_linear_call


def create_issue_ai(
    title: str,
    description: str,
    project_name: str,
    assignee_name: str,
    labels,
    team_name: str = "",
):
    print("Validating the renewed inputs")

    if not title:
        raise ValueError("Title cannot be empty")

    if not description:
        raise ValueError("Title cannot be empty")

    if team_name:
        team_object = check_and_extract_team(team_name)
        print(team_object)

    if project_name:
        project_object = check_and_extract_project(project_name)
        print(project_object)

    if assignee_name:
        assignee_object = check_and_extract_assignee(assignee_name)
        print(assignee_object)

    if labels:
        label_objects = check_and_extract_labels(labels)
        print(label_objects)

    create_issue_with_valid_inputs(title, description, team_object, project_object, assignee_object, label_objects)


def create_issue_with_valid_inputs(
    title, description, team_object, project_object, assignee_object, label_objects
):
    print(f"The title is {title}")
    print(f"The description is {description}")
    print(f"The team is {team_object}")
    print(f"The project is {project_object}")
    print(f"The assignee is {assignee_object}")
    print(f"The labels are {label_objects}")


def check_and_extract_team(team_name: str):
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
    if response:
        teams_list = response["data"]["teams"]["nodes"]
        if len(teams_list) == 0:
            raise ValueError("No team found with the given name")
        if len(teams_list) > 1:
            raise ValueError("More than one team found with the given name")
        return teams_list

    return None


def check_and_extract_project(project_name: str):
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
    if response:
        project_list = response["data"]["projects"]["nodes"]
        if len(project_list) == 0:
            raise ValueError("No project found with the given name")
        if len(project_list) > 1:
            raise ValueError("More than one project found with the given name")
        return project_list

    return None


def check_and_extract_assignee(assignee_name: str):
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
    if response:
        users_list = response["data"]["users"]["nodes"]
        if len(users_list) == 0:
            raise ValueError("No user found with the given name")
        if len(users_list) > 1:
            raise ValueError("More than one user found with the given name")
        return users_list

    return None


def check_and_extract_labels(labels):
    try:
        label_list = []
        for label in labels:
            label = check_and_extract_label(label)
            label_list.append(label)
        return label_list
    except ValueError as e:
        raise ValueError(e.args[0])


def check_and_extract_label(label):
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
    if response:
        label_list = response["data"]["issueLabels"]["nodes"]
        if len(label_list) == 0:
            raise ValueError(f"No labels found with the name {label}")
        return label_list

    return None
