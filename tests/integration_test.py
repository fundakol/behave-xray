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
    assert '3 scenarios passed, 1 failed, 0 skipped' in process.stdout, process.stdout
