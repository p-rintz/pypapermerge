"""
Provides an entrypoint to the endpoints for the api client.

The module contains the following functions:

- `endpoint()` - Returns the api endpoint URL
- `create_token(username, password)` - Creates an API token and returns the requests reponse
"""
from __future__ import annotations

import requests
from .endpoints import (
    Documents,
    Nodes
)
from json import loads
from loguru import logger


class Api(object):
    """Main Class everything branches off of"""
    def __init__(self, url: str, token: str | None = None):
        logger.trace(f'URL is: {url}')
        self.apiurl = f'{url if url[-1] != "/" else url[:-1]}/api'
        self.token = token
        self.documents = Documents(self)
        self.nodes = Nodes(self)

    def endpoint(self) -> str:
        """Returns the api endpoint URL"""
        api_url = self.apiurl
        return api_url

    def create_token(self, username: str, password: str) -> requests.Response:
        """Creates an API token if needed"""
        response = requests.post(f'{self.apiurl}/auth/login/', json={'username': username, 'password': password})
        self.token = loads(response.content.decode())['token']

        return response
