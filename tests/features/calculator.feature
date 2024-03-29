@jira.test_plan('JIRA-1')
Feature: Calculator
  description
  further description

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
  Scenario: Add two numbers
    When I add 5 and 5
    Then result is 10

  Scenario: Add two numbers without jira id
    When I add 5 and 7
    Then result is 12

  @jira.testcase('JIRA-34')
  Scenario Outline: Add two numbers: <first> and <second>
    When I add <first> and <second>
    Then result is <result>

    Examples:
      | first | second | result |
      | 1     | 2      | 3      |
      | 2     | 5      | 8      |
