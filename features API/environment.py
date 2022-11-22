import requests
import json
from pathlib import Path

project_path = Path.cwd()
file_path = project_path.joinpath("creds.json")


def before_all(context):
    with open(file_path, "r") as f:
        login_variables = json.load(f)
        context.login_variables = login_variables
        context.admin_credentials = (login_variables["admin_login"], login_variables["admin_password"])
        context.payload = {
        "username": login_variables["new_user_name"],
        "email": login_variables["new_user_email"]
    }


def after_scenario(context, scenario):
    user_id = context.response.json()["url"]
    requests.delete(user_id, auth=context.admin_credentials)

