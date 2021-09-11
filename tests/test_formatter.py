import pytest

from behave_xray.helper import get_test_execution_key_from_tag, get_test_plan_key_from_tag, get_testcase_key_from_tag, \
    get_overall_status
from behave_xray.model import XrayStatus


@pytest.mark.parametrize(
    'tag, jira_id',
    [("jira.test_plan('JIRA-10')", 'JIRA-10'),
     ("JIRA.TEST_PLAN('JIRA-10')", 'JIRA-10')]
)
def test_test_plan_tag_parser(tag, jira_id):
    assert get_test_plan_key_from_tag(tag) == jira_id


@pytest.mark.parametrize(
    'tag, jira_id',
    [("jira.testcase('JIRA-10')", 'JIRA-10'),
     ("JIRA.TESTCASE('JIRA-10')", 'JIRA-10'),
     ('jira.testcase("JIRA-10")', 'JIRA-10'),
     ('jira.testcaseJIRA-10', 'JIRA-10'),  # outline scenario
     ("allure.testcase('JIRA-10')", 'JIRA-10')]
)
def test_test_case_tag_parser(tag, jira_id):
    assert get_testcase_key_from_tag(tag) == jira_id


@pytest.mark.parametrize(
    'tag, jira_id',
    [("jira.test_execution('JIRA-10')", 'JIRA-10'),
     ("JIRA.TEST_EXECUTION('JIRA-10')", 'JIRA-10')]
)
def test_test_execution_tag_parser(tag, jira_id):
    assert get_test_execution_key_from_tag(tag) == jira_id


@pytest.mark.parametrize(
    'statuses, status',
    [
        ([XrayStatus.FAIL, XrayStatus.PASS, XrayStatus.TODO], XrayStatus.FAIL),
        ([XrayStatus.FAIL, XrayStatus.PASS, XrayStatus.PASS], XrayStatus.FAIL),
        ([XrayStatus.FAIL, XrayStatus.TODO, XrayStatus.TODO], XrayStatus.FAIL),
        ([XrayStatus.TODO, XrayStatus.TODO, XrayStatus.TODO], XrayStatus.TODO),
        ([XrayStatus.TODO, XrayStatus.TODO, XrayStatus.EXECUTING], XrayStatus.EXECUTING),
        ([XrayStatus.PASS, XrayStatus.PASS, XrayStatus.TODO], XrayStatus.EXECUTING),
        ([XrayStatus.PASS, XrayStatus.PASS, XrayStatus.EXECUTING], XrayStatus.EXECUTING),
        ([XrayStatus.PASS, XrayStatus.PASS, XrayStatus.PASS], XrayStatus.PASS)
    ]
)
def test_overall_status(statuses, status):
    assert get_overall_status(statuses) == status
