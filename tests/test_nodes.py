from pypapermerge import tools


def test_create(setup_api, file_name):
    """Tests the API call to create a node"""

    api = setup_api

    document_node = api.nodes.create(
        file_name, "documents", api.documents.id(".home", "folders")
    )
    folder_node = api.nodes.create(
        "test", "folders", api.documents.id(".home", "folders")
    )

    assert tools.check_id(document_node)
    assert tools.check_id(folder_node)
