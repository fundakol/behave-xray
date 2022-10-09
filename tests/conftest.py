import pytest
import os

from tests.mock_server import MockServer


@pytest.fixture(scope='session', autouse=True)
def environment():
    os.environ['XRAY_API_BASE_URL'] = 'http://127.0.0.1:5002'
    os.environ['XRAY_API_USER'] = 'jirauser'
    os.environ['XRAY_API_PASSWORD'] = 'jirapassword'
    os.environ['XRAY_CLIENT_ID'] = 'client_id'
    os.environ['XRAY_CLIENT_SECRET'] = 'client_secret'


@pytest.fixture(scope='session', autouse=True)
def http_server():
    server = MockServer(5002)
    server.add_json_response(
        '/rest/raven/2.0/import/execution',
        {'testExecIssue': {'key': 'JIRA-1000'}},
        methods=('POST',)
    )
    # cloud jira:
    server.add_json_response(
        '/api/v2/import/execution',
        {'testExecIssue': {'key': 'JIRA-1000'}},
        methods=('POST',)
    )
    server.add_callback_response(
        '/api/v2/authenticate',
        lambda: 'token',
        methods=('POST',)
    )
    server.start()
    yield
    server.shutdown_server()
