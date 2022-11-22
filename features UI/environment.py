import json
import allure
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from allure_commons.types import AttachmentType

project_path = Path.cwd()
file_path = project_path.joinpath("creds.json")


def before_all(context):
    with open(file_path, "r") as f:
        login_variables = json.load(f)
        context.login_variables = login_variables

    port = 4488

    # Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')

    # Run Chrome with options
    context.driver = webdriver.Remote(
        command_executor=f'http://localhost:{port}/wd/hub',
        options=options
    )


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


def after_step(context,step):
    if step.status == 'failed':
        allure.attach(context.driver.get_screenshot_as_png(), name=f"Screenshot_of_failed_test_{context.scenario}",
                      attachment_type=AttachmentType.PNG)
        time.sleep(3)