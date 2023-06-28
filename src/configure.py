import configparser
import os


def configure_system(linear_api_token: str, openai_api_key: str, gpt_model:str) -> None:
    config = configparser.ConfigParser()

    config.add_section('linear')
    config.set('linear', 'token', linear_api_token)
    config.add_section('gpt')
    config.set('gpt', 'token', openai_api_key)
    config.set('gpt', 'model', gpt_model)

    with open(os.path.expanduser('~/.linear-cli-ai-config.ini'), 'w+') as configfile:
        config.write(configfile)
    