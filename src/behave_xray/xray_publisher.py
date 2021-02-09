import json
from typing import Union

import requests
from requests.auth import AuthBase
from behave_xray.model import TestExecution

TEST_EXEXUTION_ENDPOINT = '/rest/raven/2.0/import/execution'


class XrayError(Exception):
    """Custom exception for Jira XRAY"""


class XrayPublisher:

    def __init__(self, base_url: str, auth: Union[AuthBase, tuple]) -> None:
        self.base_url = base_url
        self.auth = auth

    @property
    def endpoint_url(self) -> str:
        return self.base_url + TEST_EXEXUTION_ENDPOINT

    def publish_data(self, url: str, auth: AuthBase, data: dict) -> dict:
        headers = {'Accept': 'application/json',
                   'Content-Type': 'application/json'}
        data = json.dumps(data)
        response = requests.request(method='POST', url=url, headers=headers, data=data, auth=auth)
        try:
            response.raise_for_status()
        except Exception as e:
            raise XrayError(e)
        return response.json()

    def publish(self, test_execution: TestExecution) -> None:
        try:
            result = self.publish_data(self.endpoint_url, self.auth, test_execution.as_dict())
        except XrayError as e:
            print('Could not publish to Jira:', e)
        else:
            key = result['testExecIssue']['key']
            print('Uploaded results to XRAY Test Execution:', key)
