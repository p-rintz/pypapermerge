def test_endpoint(setup_api):
    """Tests the correct return of the API endpoint"""
    api = setup_api
    api_url = api.endpoint()
    assert isinstance(api.endpoint(), str)
    assert "api" in api_url


def test_create_token(setup_api):
    """Tests the API call to create a token"""

    api = setup_api
    response = api.create_token("admin", "admin")

    assert isinstance(api.token, str)
    assert response.status_code == 200
