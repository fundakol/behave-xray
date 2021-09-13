import json
import logging

import requests
from requests.auth import AuthBase

from behave_xray.exceptions import XrayError

_logger = logging.getLogger(__name__)


class BearerAuth(AuthBase):
    """Bearer authentication for Xray Cloud."""

    def __init__(self, base_url: str, client_id: str, client_secret: str) -> None:
        self.base_url = base_url
        self.client_id = client_id
        self.client_secret = client_secret

    @property
    def endpoint_url(self) -> str:
        return f'{self.base_url}/api/v2/authenticate'

    def __call__(self, r: requests.PreparedRequest) -> requests.PreparedRequest:
        headers = {
            'Content-type': 'application/json',
            'Accept': 'text/plain'
        }
        auth_data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }

        try:
            response = requests.post(
                self.endpoint_url,
                data=json.dumps(auth_data),
                headers=headers
            )
        except requests.exceptions.ConnectionError as exc:
            err_message = f'ConnectionError: cannot authenticate with {self.endpoint_url}'
            _logger.exception(err_message)
            raise XrayError(err_message) from exc
        else:
            auth_token = response.text
            r.headers['Authorization'] = f'Bearer {auth_token}'
        return r
