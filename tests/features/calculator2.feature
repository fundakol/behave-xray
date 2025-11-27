@jira.test_plan('JIRA-1')
Feature: Calculator2
  Test if adding two numbers returns proper result.

  @allure.testcase('JIRA-41')
  Scenario: Add two numbers should pass
    When I add 4 and 5
    Then result is 9

  @jira.testcase('JIRA-42')
  Scenario: Add two numbers should failed
    When I add 4 and 6
    Then result is 9
