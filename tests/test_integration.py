import subprocess


def test_if_xray_formatter_publishes_results():
    process = subprocess.run(
        ['behave', 'tests', '-f', 'behave_xray:XrayFormatter'],
        capture_output=True,
        text=True
    )
    assert not process.stderr
    assert 'Uploaded results to JIRA XRAY Test Execution: JIRA-1000' in process.stdout, process.stdout
    assert '2 scenarios passed, 1 failed, 0 skipped' in process.stdout, process.stdout
