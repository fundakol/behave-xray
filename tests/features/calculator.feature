@jira.test_plan('JIRA-1')
Feature: Calculator

  @allure.testcase('JIRA-31')
  Scenario: Add two numbers should pass
    When I add 4 and 5
    Then result is 9

  @jira.testcase('JIRA-32')
  Scenario: Add two numbers should failed
    When I add 4 and 6
    Then result is 9

  @wip
  @jira.testcase('JIRA-33')
  Scenario: Add tow numbers
    When I add 5 and 5
    Then result is 10
