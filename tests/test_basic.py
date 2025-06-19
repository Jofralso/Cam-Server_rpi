import pytest
from unittest.mock import MagicMock, patch
from scripts.capture import CameraManager
from app import create_app

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_camera_manager_init():
    cm = CameraManager()
    assert cm is not None

def test_flask_index(client):
    res = client.get('/')
    assert res.status_code == 200

# Mock hardware interaction example
@patch('scripts.capture.PiCamera')
def test_capture_photo_mock(mock_camera):
    cm = CameraManager()
    cm.camera = mock_camera.return_value
    cm.take_photo('test.jpg')
    cm.camera.capture.assert_called_once_with('test.jpg')

# Hint for real hardware test (run only on Pi)
@pytest.mark.skipif(not pytest.config.getoption("--run-hw-tests"), reason="Hardware tests disabled")
def test_real_camera_capture():
    cm = CameraManager()
    cm.take_photo('/tmp/test.jpg')
    # Add assertions checking file exists, etc.
