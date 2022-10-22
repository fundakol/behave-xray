import pytest

from tests.mock_server import MockServer

BASE_API_URL = 'http://127.0.0.1:5002'


def basic_auth() -> dict:
    environ = {}
    environ['XRAY_API_BASE_URL'] = BASE_API_URL
    environ['XRAY_API_USER'] = 'jirauser'
    environ['XRAY_API_PASSWORD'] = 'jirapassword'
    return environ


def client_secret_auth() -> dict:
    environ = {}
    environ['XRAY_API_BASE_URL'] = BASE_API_URL
    environ['XRAY_CLIENT_ID'] = 'client_id'
    environ['XRAY_CLIENT_SECRET'] = 'client_secret'
    return environ


def token_auth():
    environ = {}
    environ['XRAY_API_BASE_URL'] = BASE_API_URL
    environ['XRAY_TOKEN'] = 'token'
    return environ


@pytest.fixture
def auth():
    def _auth(name):
        if name == 'basic':
            return basic_auth()
        if name == 'client_secret':
            return client_secret_auth()
        if name == 'token':
            return token_auth()

    return _auth


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
        {'key': 'JIRA-1000'},
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
