functions = [
    {
        "name": "create_issue",
        "description": "Create an issue in Linear",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "The title of the issue to be created",
                },
                "description": {
                    "type": "string",
                    "description": "The description of the issue to be created",
                },
                "team_name": {
                    "type": "string",
                    "description": "The team for which this issue is to be created.",
                },
                "project_name": {
                    "type": "string",
                    "description": "The project for which this issue is to be created.",
                },
                "assignee_name": {
                    "type": "string",
                    "description": "The user who is to be assigned this issue.",
                },
                "labels": {
                    "type": "array",
                    "description": "An array of labels for this issue.",
                    "items": {"type": "string"},
                },
            },
            "required": ["title", "description", "team_name"],
        },
    },
]
