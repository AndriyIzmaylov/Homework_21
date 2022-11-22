from behave import *
from selenium.webdriver.common.by import By


@given('the admin account is on https://www.aqa.science/')
def step_impl(context):
    pass

@given('the admin creates new user and receives user id')
def step_impl(context):
    context.driver.get("https://www.aqa.science/users")
    number = 0
    userName_field = context.driver.find_element(By.XPATH, '//*[@id="post-object-form"]/form/fieldset/div[1]/div/input')
    userEmail_field = context.driver.find_element(By.XPATH, '//*[@id="post-object-form"]/form/fieldset/div[2]/div/input')
    createUserButton = context.driver.find_element(By.XPATH, '//*[@id="post-object-form"]/form/fieldset/div[4]/button')
    userName_field.send_keys(context.login_variables["new_user_name"])
    userEmail_field.send_keys(context.login_variables["new_user_email"])
    createUserButton.click()
    status_by_xpath_from_response = context.driver.find_element(By.XPATH,
                                                               '//*[@id="content"]/div[2]/div[4]/pre/span[1]/b[1]').text
    while status_by_xpath_from_response != "HTTP 201 Created":
        number += 1
        userName_field = context.driver.find_element(By.XPATH,
                                                    '//*[@id="post-object-form"]/form/fieldset/div[1]/div/input')
        userName_field.clear()
        userEmail_field = context.driver.find_element(By.XPATH,
                                                     '//*[@id="post-object-form"]/form/fieldset/div[2]/div/input')

        userEmail_field.clear()
        createUserButton = context.driver.find_element(By.XPATH,
                                                      '//*[@id="post-object-form"]/form/fieldset/div[4]/button')
        userName_field.send_keys(f'{context.login_variables["new_user_name"]}{number}')
        userEmail_field.send_keys(context.login_variables["new_user_email"])
        createUserButton.click()
        status_by_xpath_from_response = context.driver.find_element(By.XPATH,
                                                                   '//*[@id="content"]/div[2]/div[4]/pre/span[1]/b[1]').text
    context.status_created_by_xpath_from_response = status_by_xpath_from_response
    context.user_id_after_create = context.driver.find_element(By.XPATH,
                                                               '//*[@id="content"]/div[2]/div[4]/pre/span[1]/span[3]/a').text


@when('admin creates a user')
def step_impl(context):
    context.execute_steps(u"""
           given the admin creates new user and receives user id           
           """)


@then('user is created successfully')
def step_impl(context):
    assert context.status_created_by_xpath_from_response == "HTTP 201 Created"


@when('admin gets user by id')
def step_impl(context):
    context.driver.get(context.user_id_after_create)
    context.user_status_for_read = context.driver.find_element(By.XPATH,
                                                               '//*[@id="content"]/div[2]/div[4]/pre/span[1]/b[1]').text


@then('user is found')
def step_impl(context):
    assert context.user_status_for_read == "HTTP 200 OK"


@when('admin sets a new user name')
def step_impl(context):
    context.driver.get(context.user_id_after_create)
    new_user_name_for_update = context.driver.find_element(By.XPATH,
                                                          '//*[@id="put-object-form"]/form/fieldset/div[1]/div/input')
    new_user_name_for_update.clear()
    new_user_name_for_update.send_keys(context.login_variables["updated_name"])
    put_button = context.driver.find_element(By.XPATH, '//*[@id="put-object-form"]/form/fieldset/div[4]/button')
    put_button.click()
    context.driver.get(context.user_id_after_create)
    context.user_upd = context.driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[4]/pre/span[14]').text


@then('user is successfully updated')
def step_impl(context):
    assert context.user_upd == f'"{context.login_variables["updated_name"]}"'


@when('admin deletes a user')
def step_impl(context):
    context.driver.get(context.user_id_after_create)
    context.driver.find_element(By.XPATH, '//*[@id="content"]/div[1]/button').click()
    context.driver.find_element(By.XPATH, '//*[@id="deleteModal"]/div/div/div[2]/form/button').submit()
    context.status_by_xpath_after_delete = context.driver.find_element(By.XPATH,
                                                              '//*[@id="content"]/div[2]/div[4]/pre/span/b[1]').text

@then('user is successfully deleted')
def step_impl(context):
    assert context.status_by_xpath_after_delete == 'HTTP 200 OK'
