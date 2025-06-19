import pytest
from unittest.mock import MagicMock, patch
from scripts.inky_display import InkyManager

@patch('scripts.inky_display.InkyPHAT')
def test_inky_display_messages(mock_inkyphat):
    im = InkyManager()
    im.inky = mock_inkyphat.return_value

    im.show_message("Hello World")
    im.inky.set_border.assert_called()
    im.inky.show.assert_called()

    im.show_photo_count(10)
    im.show_gif_count(5)
