from behave import *
import requests


@given('the admin account is on https://www.aqa.science/ using API')
def step_impl(context):
    pass


@given('the admin creates new user and receives user using API')
def step_impl(context):
    response = requests.post(context.login_variables["url"], auth=context.admin_credentials, data=context.payload)
    while response.status_code != 201:
        context.payload["username"] = context.payload["username"] + "1"
        response = requests.post(context.login_variables["url"], auth=context.admin_credentials, data=context.payload)
    context.response = response


@when('admin creates a user using API')
def step_impl(context):
    context.execute_steps(u"""
           given the admin creates new user and receives user using API           
           """)


@then('user is created successfully using API')
def step_impl(context):
    assert 201 == context.response.status_code


@when('admin gets user by id using API')
def step_impl(context):
    user_id = context.response.json()["url"]
    context.get_response = requests.get(user_id, auth=context.admin_credentials)


@then('user is found using API')
def step_impl(context):
    assert context.get_response.status_code == 200
    assert context.get_response.json()["username"] == context.payload["username"]


@when('admin sets a new user name using API')
def step_impl(context):
    context.update_user = requests.put(context.response.json()["url"], auth=context.admin_credentials, data={
        "username": context.login_variables["var_for_update"], "email": context.login_variables["new_user_email"]})


@then('user is successfully updated using API')
def step_impl(context):
    assert context.update_user.status_code == 200
    assert context.update_user.json()["username"] == context.login_variables["var_for_update"]


@when('admin deletes a user using API')
def step_impl(context):
    user_id = context.response.json()["url"]
    context.deleted_user = requests.delete(user_id, auth=context.admin_credentials)


@then('user is successfully deleted using API')
def step_impl(context):
    assert context.deleted_user.status_code == 204
