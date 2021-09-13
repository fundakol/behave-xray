import subprocess

import pytest


@pytest.mark.parametrize(
    'formatter',
    [
        'behave_xray:XrayFormatter',
        'behave_xray:XrayCloudFormatter'
    ]
)
def test_if_xray_formatter_publishes_results(formatter):
    process = subprocess.run(
        ['behave', 'tests', '-f', formatter],
        capture_output=True,
        text=True
    )
    assert not process.stderr
    assert 'Uploaded results to JIRA XRAY Test Execution: JIRA-1000' in process.stdout, process.stdout
    assert '2 scenarios passed, 1 failed, 0 skipped' in process.stdout, process.stdout
