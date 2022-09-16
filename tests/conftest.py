from pprint import pprint

import pytest

from pypapermerge import Api


@pytest.fixture
def file_name():
    """Returns a file name as string"""
    return "test.pdf"


@pytest.fixture(scope="session")
def setup_api():
    """Setups API and creates a token"""
    api = Api("http://127.0.0.1")
    api.create_token("admin", "admin")
    return api


@pytest.fixture
def delete_all(setup_api):
    """Deletes all documents on the server"""
    api = setup_api
    all_documents = api.documents.all()
    for doc in all_documents:
        api.documents.delete(doc)
