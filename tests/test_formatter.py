import pytest

from behave_xray.formatter import get_test_case_tag
from behave_xray.formatter import get_test_execution_tag
from behave_xray.formatter import get_test_plan_tag


@pytest.mark.parametrize('tag, jira_id',
                         [("jira.test_plan('JIRA-10')", 'JIRA-10'),
                          ("jira.testplan('JIRA-10')", 'JIRA-10'),
                          ("JIRA.TESTPLAN('JIRA-10')", 'JIRA-10')])
def test_test_plan_tag_parser(tag, jira_id):
    assert get_test_plan_tag(tag) == jira_id


@pytest.mark.parametrize('tag, jira_id',
                         [("jira.test_case('JIRA-10')", 'JIRA-10'),
                          ("jira.testcase('JIRA-10')", 'JIRA-10'),
                          ("JIRA.TESTCASE('JIRA-10')", 'JIRA-10'),
                          ('jira.testcase("JIRA-10")', 'JIRA-10'),
                          ("allure.testcase('JIRA-10')", 'JIRA-10'),
                          ("jira.testcaseJIRA-10", 'JIRA-10')])  # scenario outline
def test_test_case_tag_parser(tag, jira_id):
    assert get_test_case_tag(tag) == jira_id


@pytest.mark.parametrize('tag, jira_id',
                         [("jira.test_execution('JIRA-10')", 'JIRA-10'),
                          ("jira.testexecution('JIRA-10')", 'JIRA-10'),
                          ("JIRA.TEST_EXECUTION('JIRA-10')", 'JIRA-10')])
def test_test_execution_tag_parser(tag, jira_id):
    assert get_test_execution_tag(tag) == jira_id
