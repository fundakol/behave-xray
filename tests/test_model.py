import datetime as dt
from unittest.mock import patch

import pytest
from behave_xray.formatter import TestExecution as _TestExecution
from behave_xray.formatter import TestCase as _TestCase


@pytest.fixture
def testcase():
    testcase = _TestCase(test_key='JIRA-1', comment='Test', status='PASS')
    return testcase


@pytest.fixture
def outline_testcase():
    testcase = _TestCase(test_key='JIRA-1', comment='Test', status='FAIL',
                         examples=['PASS', 'FAIL'])
    return testcase


def test_testcase_output_dictionary(testcase):
    assert testcase.as_dict() == {'testKey': 'JIRA-1', 'comment': 'Test',
                                  'examples': [], 'status': 'PASS'}


def test_testcase_output_dictionary_with_examples(outline_testcase):
    assert outline_testcase.as_dict() == {'testKey': 'JIRA-1', 'comment': 'Test',
                                          'examples': ['PASS', 'FAIL'], 'status': 'FAIL'}


def test_test_execution_output_dictionary(testcase):
    testdt = dt.datetime(2021, 4, 23, 16, 30, 2, 0, tzinfo=dt.timezone.utc)
    with patch('datetime.datetime') as dt_mock:
        dt_mock.now.return_value = testdt
        te = _TestExecution()
        te.tests = [testcase]
        assert te.as_dict() == {'info': {'finishDate': '2021-04-23T16:30:02+0000',
                                         'startDate': '2021-04-23T16:30:02+0000'},
                                'tests': [{'comment': 'Test',
                                           'examples': [],
                                           'status': 'PASS',
                                           'testKey': 'JIRA-1'}]}


def test_test_execution_output_dictionary_with_test_plan_id(testcase):
    testdt = dt.datetime(2021, 4, 23, 16, 30, 2, 0, tzinfo=dt.timezone.utc)
    with patch('datetime.datetime') as dt_mock:
        dt_mock.now.return_value = testdt
        te = _TestExecution(test_plan_key='Jira-10')
        te.tests = [testcase]
        assert te.as_dict() == {'info': {'finishDate': '2021-04-23T16:30:02+0000',
                                         'startDate': '2021-04-23T16:30:02+0000',
                                         'testPlanKey': 'Jira-10'},
                                'tests': [{'comment': 'Test',
                                           'examples': [],
                                           'status': 'PASS',
                                           'testKey': 'JIRA-1'}]}


def test_test_execution_output_dictionary_with_test_execution_id(testcase):
    testdt = dt.datetime(2021, 4, 23, 16, 30, 2, 0, tzinfo=dt.timezone.utc)
    with patch('datetime.datetime') as dt_mock:
        dt_mock.now.return_value = testdt
        te = _TestExecution(test_plan_key='Jira-10', test_execution_key='JIRA-20')
        te.tests = [testcase]
        assert te.as_dict() == {'testExecutionKey': 'JIRA-20',
                                'info': {'finishDate': '2021-04-23T16:30:02+0000',
                                         'startDate': '2021-04-23T16:30:02+0000',
                                         'testPlanKey': 'Jira-10'},
                                'tests': [{'comment': 'Test',
                                           'examples': [],
                                           'status': 'PASS',
                                           'testKey': 'JIRA-1'}]}


def test_test_case_status_validation():
    with pytest.raises(ValueError):
        _TestCase('Jira-1', status='TO-DO')


def test_test_case_status_validation_for_assigning():
    test_case = _TestCase('Jira-1')
    with pytest.raises(ValueError):
        test_case.status = 'TO-DO'
