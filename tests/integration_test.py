import json
import os
import subprocess

import pytest


@pytest.mark.parametrize(
    'formatter, auth_type',
    [
        ('behave_xray:XrayFormatter', 'basic'),
        ('behave_xray:XrayFormatter', 'token'),
        ('behave_xray:XrayCloudFormatter', 'client_secret')
    ]
)
def test_if_xray_formatter_publishes_results(formatter, auth_type, auth):
    env = dict(os.environ).copy()
    env.update(auth(auth_type))

    process = subprocess.run(
        ['behave', 'tests', '-f', formatter],
        capture_output=True,
        text=True,
        env=env
    )
    assert not process.stderr
    assert 'Uploaded results to JIRA XRAY Test Execution: JIRA-1000' in process.stdout, process.stdout
    assert '5 scenarios passed, 3 failed, 0 skipped' in process.stdout, process.stdout


def test_if_xray_formatter_results_matches_expected_format(auth, tmp_path):
    report_path = tmp_path / 'xray.json'
    env = dict(os.environ).copy()
    env.update(auth('basic'))

    process = subprocess.run(
        ['python', '-m', 'behave', 'tests', '-f', 'behave_xray:XrayFormatter', '-o', report_path.name],
        capture_output=True,
        text=True,
        env=env
    )
    print(process.stdout)
    assert not process.stderr
    assert 'Uploaded results to JIRA XRAY Test Execution: JIRA-1000' in process.stdout
    assert '5 scenarios passed, 3 failed, 0 skipped' in process.stdout

    with open(report_path.name, 'r') as f:
        report = json.load(f)

    assert len(report) == 1
    assert 'tests' in report[0]
    assert report[0]['tests'] == [
            {
                'testKey': 'JIRA-31',
                'status': 'PASS',
                'comment': '',
                'examples': []
            },
            {
                'testKey': 'JIRA-32',
                'status': 'FAIL',
                'comment': 'Assertion Failed: Not equal',
                'examples': []
            },
            {
                'testKey': 'JIRA-33',
                'status': 'PASS',
                'comment': '',
                'examples': []
            },
            {
                'testKey': 'JIRA-34',
                'status': 'FAIL',
                'comment': '',  # FIXME: missing assertion message
                'examples': ['PASS', 'FAIL']
            },
            {
                'testKey': 'JIRA-41',
                'status': 'PASS',
                'comment': '',
                'examples': []
            },
            {
                'testKey': 'JIRA-42',
                'status': 'FAIL',
                'comment': 'Assertion Failed: Not equal',
                'examples': []
            }
        ]
