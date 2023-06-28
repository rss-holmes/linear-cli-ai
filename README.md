# linear-cli
An AI based CLI for the linear app

# Installation

Installation of linear-cli-ai and its dependencies require ``python`` and ``pip``. To ensure smooth installation,
it's recommended to use:

- ``python``: 3.8.10 or greater
- ``pip``: 9.0.2 or greater

The safest way to install globally is to use

```

   $ python -m pip install awscli

```

or for your user:

```

   $ python -m pip install --user awscli

```

If you have the linear-cli-ai package installed and want to upgrade to the
latest version, you can run:

```

   $ python -m pip install --upgrade awscli

```

# Configuration

Before using linear-cli-ai, you need to configure a few keys.
You can do this in several ways:

-  Configuration command
-  Environment variables
-  Config file

The quickest way to get started is to run the ``linear-cli-ai configure`` command:

```
$ linear-cli-ai configure
  Provide the following details : 
   Linear API Token : MY_LINEAR_TOKEN
   OpenAI API Key : MY_OPENAI_KEY
   Select the model you will use : gpt4 or gpt-3.5-turbo-0613

```

To use environment variables, do the following:

```

   $ export LINEAR_TOKEN=<linear_token>
   $ export GPT_MODEL=<gpt_model>
   $ export OPENAI_API_KEY=<openai_api_key>

```

To use a config file, create an INI formatted file like this:

```
  [linear]
  token = <linear_token>
  
  [gpt]
  token = <openai_api_key>
  model = <gpt_model>

```
and place it in ``~/.linear-cli-ai.ini`` (or in ``%UserProfile%\.linear-cli-ai.ini``
on Windows).

# Sample Usage

To view help documentation type :

```
$ linear-cli-ai help

```

To use ai to perform actions on linear:

```
$ linear-cli-ai ai

```

To create an issue via options on linear :

```
$ linear-cli-ai create-issue

```
## Sample command for creating issue using ai
Create an issue with description 'Rewrite the print service with queue system'
and title as 'Print Service v2.0' and team as 'engineering' and assign it to 'Rohan'
and add labels 'bug' and 'high priority' and add it to project 'Print Service'


