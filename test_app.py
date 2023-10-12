from unittest.mock import patch

import pytest

from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


# TODO: Move tests to test directory
@patch('app.OAuth2Session.authorization_url')
def test_index_route(mock_oauth2_session, client):
    mock_oauth2_session.return_value = ('http://example.com/auth', 'state')
    response = client.get('/')

    assert response.status_code == 302
    assert 'http://example.com/auth' in response.text

    # Check if the session variable 'oauth_state' is set
    with client.session_transaction() as session:
        assert 'oauth_state' in session
