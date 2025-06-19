import io
import os
import pytest
from app import create_app

@pytest.fixture
def app(tmp_path):
    # Prepare test photos directory
    photos_dir = tmp_path / "photos"
    photos_dir.mkdir()
    # Create dummy photo file
    dummy_photo = photos_dir / "test.jpg"
    dummy_photo.write_bytes(b"dummydata")

    app = create_app()
    app.config['TESTING'] = True
    app.config['PHOTO_DIR'] = str(photos_dir)
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'test.jpg' in response.data  # file listed on page

def test_photo_file(client):
    response = client.get('/photos/test.jpg')
    assert response.status_code == 200
    assert response.data == b'dummydata'

def test_photo_file_not_found(client):
    response = client.get('/photos/missing.jpg')
    assert response.status_code == 404

def test_api_status(client):
    response = client.get('/api/status')
    assert response.status_code == 200
    json_data = response.get_json()
    assert 'photos_taken' in json_data
    assert 'gifs_taken' in json_data
