import pytest
from unittest.mock import MagicMock, patch
from scripts.capture import CameraManager

@patch('scripts.capture.PiCamera')
def test_take_photo(mock_picamera):
    cm = CameraManager()
    cm.camera = mock_picamera.return_value

    filename = 'photo.jpg'
    cm.take_photo(filename)

    cm.camera.capture.assert_called_once_with(filename)

@patch('scripts.capture.PiCamera')
def test_take_gif(mock_picamera):
    cm = CameraManager()
    cm.camera = mock_picamera.return_value
    cm.take_photo = MagicMock()

    filename = 'anim.gif'
    cm.take_gif(filename)

    # Should call take_photo multiple times
    assert cm.take_photo.call_count == 5
    calls = [call.args[0] for call in cm.take_photo.call_args_list]
    for i in range(5):
        assert f'frame_{i}' in calls[i]
