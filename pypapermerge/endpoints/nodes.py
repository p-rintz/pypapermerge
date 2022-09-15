import requests
from pypapermerge import tools
import json
from loguru import logger


class Nodes(object):
    def __init__(self, api):  # type: ignore
        self.api = api

    def create(self, name: str, content_type: str, parent_folder_id: str) -> str:
        tools.check_ctype(content_type)
        tools.check_id(parent_folder_id)
        headers = {
            'Authorization': f'Token {self.api.token}',
            'Content-Type': 'application/vnd.api+json'
        }
        data = {
            'data': {
                'type': content_type,
                'attributes': {
                    'title': name
                },
                'relationships': {
                    'parent': {
                        'data': {
                            'type': 'folders',
                            'id': parent_folder_id
                        }
                    }
                }
            }
        }
        response = requests.post(f'{self.api.apiurl}/nodes/', headers=headers, json=data)
        logger.trace(f'nodes.create response is: {response}')
        node_id = json.loads(response.content)['data']['id']
        return node_id
