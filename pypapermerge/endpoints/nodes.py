"""Nodes endpoint API calls"""
import json

import requests
from loguru import logger

from pypapermerge import tools


class Nodes:  # pylint: disable=R0903
    """
    Class that implements the nodes endpoints
    """

    def __init__(self, api):  # type: ignore
        self.api = api

    def create(self, name: str, content_type: str, parent_folder_id: str) -> str:
        """
        Creates a node, based on the arguments given.
        Args:
            name: Name of node that should be created
            content_type: Either 'documents' or 'folders'
            parent_folder_id: ID of the parent folder the node should be created in
        Returns:
            node_id: ID of the created node
        """
        tools.check_ctype(content_type)
        tools.check_id(parent_folder_id)
        headers = {
            "Authorization": f"Token {self.api.token}",
            "Content-Type": "application/vnd.api+json",
        }
        data = {
            "data": {
                "type": content_type,
                "attributes": {"title": name},
                "relationships": {
                    "parent": {"data": {"type": "folders", "id": parent_folder_id}}
                },
            }
        }
        response = requests.post(
            f"{self.api.apiurl}/nodes/", headers=headers, json=data, timeout=5
        )
        logger.trace(f"nodes.create response is: {response}")
        node_id = json.loads(response.content)["data"]["id"]
        return node_id
