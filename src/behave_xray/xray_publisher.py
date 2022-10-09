import logging
from typing import Union

import requests
from requests.auth import AuthBase

from behave_xray.exceptions import XrayError

TEST_EXECUTION_ENDPOINT = '/rest/raven/2.0/import/execution'
TEST_EXECUTION_ENDPOINT_CLOUD = '/api/v2/import/execution'

_logger = logging.getLogger(__name__)


class XrayPublisher:

    def __init__(self, base_url: str, endpoint: str, auth: Union[AuthBase, tuple]) -> None:
        if base_url.endswith('/'):
            base_url = base_url[:-1]
        self.base_url = base_url
        self.endpoint = endpoint
        self.auth = auth

    @property
    def endpoint_url(self) -> str:
        return self.base_url + self.endpoint

    def publish_xray_results(self, url: str, auth: AuthBase, data: dict) -> dict:
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        try:
            response = requests.request(method='POST', url=url, headers=headers, json=data, auth=auth)
        except requests.exceptions.ConnectionError as e:
            message = f'ConnectionError: JIRA service on {self.base_url}'
            _logger.exception(message)
            raise XrayError(message) from e
        else:
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                err_message = (f'HTTPError: Could not post to JIRA service at {url}. '
                               f'Response status code: {response.status_code}')
                _logger.exception(err_message)
                if 'error' in response.json():
                    server_return_error = f"Error message from server: {response.json()['error']}"
                    err_message += '\n' + server_return_error
                    _logger.error(server_return_error)
                raise XrayError(err_message) from e
            else:
                return response.json()

    def publish(self, test_execution: dict) -> bool:
        try:
            result = self.publish_xray_results(self.endpoint_url, self.auth, test_execution)
        except XrayError as e:
            _logger.error('Could not publish results to Jira XRAY')
            _logger.error(e.message)
            return False
        else:
            key = result['testExecIssue']['key']
            print('Uploaded results to JIRA XRAY Test Execution:', key)
            return True
