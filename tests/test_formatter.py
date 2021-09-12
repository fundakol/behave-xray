import datetime as dt
from unittest.mock import MagicMock, patch

import pytest
from behave.model_core import Status

from behave_xray.formatter import XrayFormatter, TCStatus
from behave_xray.helper import (
    get_test_execution_key_from_tag,
    get_test_plan_key_from_tag,
    get_testcase_key_from_tag,
    get_overall_status
)
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
    'statuses, expected_status',
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
def test_overall_status(statuses, expected_status):
    assert get_overall_status(statuses) == expected_status, f'Failed for {statuses}'


def test_xray_formatter_returns_correct_dictionary():
    mock_stream = MagicMock()
    mock_config = MagicMock()
    testdt = dt.datetime(2021, 4, 23, 16, 30, 2, 0, tzinfo=dt.timezone.utc)
    with patch('datetime.datetime') as dt_mock:
        dt_mock.now.return_value = testdt
        formatter = XrayFormatter(mock_stream, mock_config)

        formatter.testcases = {
            'JIRA-1': TCStatus('JIRA-1', statuses=[XrayStatus.PASS]),
            'JIRA-2': TCStatus('JIRA-2', statuses=[XrayStatus.PASS])
        }
        formatter.collect_tests()
        expected_output = {
            'info': {
                'finishDate': '2021-04-23T16:30:02+0000',
                'startDate': '2021-04-23T16:30:02+0000'
            },
            'tests': [
                {
                    'comment': '',
                    'examples': [],
                    'status': 'PASS',
                    'testKey': 'JIRA-1'
                },
                {
                    'comment': '',
                    'examples': [],
                    'status': 'PASS',
                    'testKey': 'JIRA-2'
                }
            ]
        }

        assert formatter.test_execution.as_dict() == expected_output


def test_xray_formatter_returns_correct_dictionary_for_outline_scenario():
    mock_stream = MagicMock()
    mock_config = MagicMock()
    testdt = dt.datetime(2021, 4, 23, 16, 30, 2, 0, tzinfo=dt.timezone.utc)
    with patch('datetime.datetime') as dt_mock:
        dt_mock.now.return_value = testdt
        formatter = XrayFormatter(mock_stream, mock_config)

        formatter.testcases = {
            'JIRA-1': TCStatus(
                'JIRA-1',
                statuses=[XrayStatus.PASS, XrayStatus.PASS],
                is_outline=True
            ),
            'JIRA-2': TCStatus(
                'JIRA-2',
                statuses=[XrayStatus.PASS, XrayStatus.FAIL],
                is_outline=True)
        }
        formatter.collect_tests()
        expected_output = {
            'info': {
                'finishDate': '2021-04-23T16:30:02+0000',
                'startDate': '2021-04-23T16:30:02+0000'
            },
            'tests': [
                {
                    'comment': '',
                    'examples': ['PASS', 'PASS'],
                    'status': 'PASS',
                    'testKey': 'JIRA-1'
                },
                {
                    'comment': '',
                    'examples': ['PASS', 'FAIL'],
                    'status': 'FAIL',
                    'testKey': 'JIRA-2'
                }
            ]
        }

        assert formatter.test_execution.as_dict() == expected_output
