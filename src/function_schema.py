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
                    "enum": ["engineering", "qa", "design", "data", "product"],
                    "description": "The team for which this issue is created.",
                },
                "project_name": {
                    "type": "string",
                    "enum": [
                        "typeahead revamp",
                        "nlv revamp v1",
                        "nlv revamp v2",
                        "gmail integration",
                    ],
                    "description": "The project for which this issue is created.",
                },
                "assignee_name": {
                    "type": "string",
                    "enum": ["rohan", "sharad", "ajwad", "sagar"],
                    "description": "The user who is assigned this issue.",
                },
                "labels": {
                    "type": "array",
                    "enum": [
                        "IA-Retention",
                        "IA-Monetization",
                        "IA-Activation",
                        "IA-Referral",
                    ],
                    "description": "An array of labels for this issue.",
                    "items": {"type": "string"},
                },
            },
            "required": ["title", "description"],
        },
    },
]
