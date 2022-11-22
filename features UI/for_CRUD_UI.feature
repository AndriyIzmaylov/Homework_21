Feature: test CRUD by webdriver

  Scenario: Create user
    Given the admin account is on https://www.aqa.science/
    When admin creates a user
    Then user is created successfully


  Scenario: Read a user
    Given the admin creates new user and receives user id
    When admin gets user by id
    Then user is found

  Scenario: Update a user
    Given the admin creates new user and receives user id
    When admin sets a new user name
    Then user is successfully updated


  Scenario: Delete a user
    Given the admin creates new user and receives user id
    When admin deletes a user
    Then user is successfully deleted