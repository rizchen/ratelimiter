import pytest
from app import app as flask_app
import json

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.mark.test_index
def test_index(app, client):
    res = client.get('/')
    assert res.status_code == 200

@pytest.mark.test_ip_watcher
def test_index(app, client):
    mock_request_headers = {}
    mock_request_data = {
        "n": '1',
        'check_exist': '1'
    }
    res = client.get('/ip_watcher', data=json.dumps(mock_request_data), headers=mock_request_headers)
    assert res.status_code == 200
