Feature: Login to Stock Trader
    As a user
    I want to login to the stock trader application
    So that I can access my account

    Scenario: Successful login with valid credentials
        Given I am on the login page
        When I enter valid credentials
        And I click the continue button
        Then I should see my account number displayed
