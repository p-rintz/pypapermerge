import pytest

from pypapermerge import tools


def test_all(setup_api, file_name, delete_all):
    """Tests the API call that returns all document information"""

    api = setup_api
    # noinspection PyStatementEffect
    delete_all
    api.nodes.create(file_name, "documents", api.documents.id(".home", "folders"))

    all_documents = api.documents.all()
    idd = list(all_documents.keys())[0]
    assert type(all_documents) == dict
    assert tools.check_id(idd)
    assert all_documents[idd]["title"] == "test.pdf"


def test_id(setup_api, file_name, delete_all):
    api = setup_api
    # noinspection PyStatementEffect
    delete_all
    idd = api.documents.id(file_name, "documents")
    assert idd is None
    api.nodes.create(file_name, "documents", api.documents.id(".home", "folders"))
    idd = api.documents.id(file_name, "documents")
    assert tools.check_id(idd)
    api.nodes.create(file_name, "documents", api.documents.id(".home", "folders"))
    idl = api.documents.id(file_name, "documents")
    assert type(idl) == list
    for i in idl:
        assert tools.check_id(i)


def test_upload(setup_api, file_name, delete_all):
    api = setup_api
    # noinspection PyStatementEffect
    delete_all
    response = api.documents.upload(f"tests/{file_name}")
    assert response.status_code == 201
    response = api.documents.upload(f"tests/{file_name}")
    assert response.status_code == 201
    with pytest.raises(
        FileNotFoundError, match="File non-existing.pdf does not exist."
    ):
        api.documents.upload(f"non-existing.pdf")
