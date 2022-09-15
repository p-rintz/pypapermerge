from __future__ import annotations

import requests
import json
import os
from loguru import logger
from collections import defaultdict
from pypapermerge import tools
from mimetypes import guess_type


class Documents(object):
    """
    Class that implements the document endpoints
    """
    def __init__(self, api):  # type: ignore
        self.api = api

    def all(self) -> dict:
        """
        Returns all documents on the server
        Returns:
            return_dict: Key: ID of documents, Value (dict): attributes of documents
        """
        headers = {
            'Authorization': f'Token {self.api.token}',
        }
        response = requests.get(f'{self.api.apiurl}/documents/', headers=headers)
        json_content = json.loads(response.content)
        return_dict = {}
        for i in json_content['data']:
            return_dict.update({i['id']: i['attributes']})
        return return_dict

    def id(self, name: str, content_type: str) -> str | list[str] | None:
        """
        Returns the ID of either documents or folders type
        Args:
            name: Name of either a document or folder
            content_type: Can be one of "documents" or "folders", based on the type of content to id
        Returns:
            None (None): If no fitting document/folder was found
            return_id (str): If one fitting document/folder was found
            return_id (list): If multiple fitting documents/folders were found
        """
        tools.check_ctype(content_type)
        reverse_dict = self._reverse_list(content_type)
        if name in reverse_dict:
            logger.trace(f'ID of {name} is: {reverse_dict[name]}')
            return_id = reverse_dict[name]
            if len(return_id) == 1:
                return return_id[0]
            else:
                return return_id
        else:
            return None

    def upload(self, file: str, folder: str = '.inbox', isid: bool = False) -> requests.Response:
        """
        Uploads a file to a folder.
        Args:
            file: Path to a file to be uploaded
            folder: Can be either a folder name or ID.
            isid: Bool when folder is an ID
        Returns:
             Upload response
        """
        if not os.path.exists(file):
            raise FileNotFoundError(f'File {file} does not exist.')
        file_name = os.path.basename(file)
        if self.id(file_name, 'documents'):
            file_id = self.id(file_name, 'documents')
            tools.check_id(file_id)
        else:
            if isid:
                folder_id: str = folder
            else:
                folder_id = self.id(folder, 'folders')  # type: ignore
            tools.check_id(folder_id)
            file_id = self.api.nodes.create(file_name, 'documents', folder_id)
        url = f'{self.api.apiurl}/documents/{file_id}/upload/{file_name}'
        mimetype = guess_type(file_name)[1]
        headers: dict = {
            'Content-Disposition': f'attachment; filename={file_name}',
            'Content-Type': mimetype,
            'Authorization': f'Token {self.api.token}'
        }
        with open(file, 'rb') as fobj:
            response = requests.put(url, data=fobj, headers=headers)
        return response

    def delete(self, idd: str) -> bool:
        """
        Deletes the document identified by the ID given to the function
        Arguments:
            idd: ID of the document to be deleted
        Returns:
            Either True or False, based on the success of deletion of the document
        """
        tools.check_id(idd)
        url = f'{self.api.apiurl}/documents/{idd}'
        headers: dict = {
            'Authorization': f'Token {self.api.token}'
        }
        response = requests.delete(url, headers=headers)
        if response.status_code == 204:
            return True
        else:
            return False

    def _reverse_list(self, content_type: str) -> dict:
        """
        Returns a reversed list of all documents, in order to find the specific ID of a document if only a name is known
        """
        tools.check_ctype(content_type)
        headers = {
            'Authorization': f'Token {self.api.token}',
        }
        if content_type == 'documents':
            url = f'{self.api.apiurl}/documents/'
        else:
            url = f'{self.api.apiurl}/folders/'
        response = requests.get(url, headers=headers)
        json_content = json.loads(response.content)
        reverse_dict = defaultdict(list)
        for i in json_content['data']:
            reverse_dict[i['attributes']['title']].append(i['id'])
        return reverse_dict
