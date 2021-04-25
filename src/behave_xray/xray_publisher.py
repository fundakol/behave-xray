import json
import logging
from typing import Union

import requests
from behave_xray.model import TestExecution
from requests.auth import AuthBase

TEST_EXEXUTION_ENDPOINT = '/rest/raven/2.0/import/execution'

logging.basicConfig()
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)


class XrayError(Exception):
    """Custom exception for Jira XRAY"""


class XrayPublisher:

    def __init__(self, base_url: str, auth: Union[AuthBase, tuple]) -> None:
        if base_url.endswith('/'):
            base_url = base_url[:-1]
        self.base_url = base_url
        self.auth = auth

    @property
    def endpoint_url(self) -> str:
        return self.base_url + TEST_EXEXUTION_ENDPOINT

    def publish_xray_results(self, url: str, auth: AuthBase, data: dict) -> dict:
        headers = {'Accept': 'application/json',
                   'Content-Type': 'application/json'}
        try:
            response = requests.request(method='POST', url=url, headers=headers, json=data, auth=auth)
        except requests.exceptions.ConnectionError as e:
            _logger.exception('ConnectionError to JIRA service %s', self.base_url)
            raise XrayError(e)
        else:
            try:
                response.raise_for_status()
            except Exception as e:
                _logger.error('Could not post to JIRA service %s. Response status code: %s',
                              self.base_url, response.status_code)
                _logger.error('Response error: %s', response.json())
                raise XrayError from e
            return response.json()

    def publish(self, test_execution: TestExecution) -> bool:
        try:
            result = self.publish_xray_results(self.endpoint_url, self.auth, test_execution.as_dict())
        except XrayError:
            _logger.error('Could not publish results to Jira XRAY')
            return False
        else:
            key = result['testExecIssue']['key']
            print('Uploaded results to JIRA XRAY Test Execution:', key)
            return True
