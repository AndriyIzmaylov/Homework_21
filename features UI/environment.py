import json
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

project_path = Path.cwd()
file_path = project_path.joinpath("creds.json")


def before_all(context):
    with open(file_path, "r") as f:
        login_variables = json.load(f)
        context.login_variables = login_variables

    context.driver = webdriver.Chrome(ChromeDriverManager().install())


def before_scenario(context, scenario):
    context.driver.get("https://www.aqa.science/api-auth/login/?next=/")
    login_field = context.driver.find_element(By.XPATH, '//*[@id="id_username"]')
    password_field = context.driver.find_element(By.XPATH, '//*[@id="id_password"]')
    login_button = context.driver.find_element(By.XPATH, '//*[@id="submit-id-submit"]')
    login_field.send_keys(context.login_variables["admin_login"])
    password_field.send_keys(context.login_variables["admin_password"])
    login_button.click()


def after_all(context):
    context.driver.close()

def after_scenario(context, scenario):
    context.driver.get(context.user_id_after_create)
    context.driver.find_element(By.XPATH, '//*[@id="content"]/div[1]/button').click()
    context.driver.find_element(By.XPATH, '//*[@id="deleteModal"]/div/div/div[2]/form/button').submit()
    context.driver.get("https://www.aqa.science/api-auth/logout/?next=/users/")