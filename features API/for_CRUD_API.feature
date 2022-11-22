Feature: test CRUD by API

  Scenario: Create user using API
    Given the admin account is on https://www.aqa.science/ using API
    When admin creates a user using API
    Then user is created successfully using API


  Scenario: Read a user using API
    Given the admin creates new user and receives user using API
    When admin gets user by id using API
    Then user is found using API

  Scenario: Update a user using API
    Given the admin creates new user and receives user using API
    When admin sets a new user name using API
    Then user is successfully updated using API


  Scenario: Delete a user using API
    Given the admin creates new user and receives user using API
    When admin deletes a user using API
    Then user is successfully deleted using API