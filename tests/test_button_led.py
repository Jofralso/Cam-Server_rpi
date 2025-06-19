import pytest
from unittest.mock import MagicMock, patch
from scripts.button_led import ButtonLedManager

@patch('scripts.button_led.GPIO')
def test_button_press_gpio(mock_gpio):
    blm = ButtonLedManager(button_pin=17, led_pins={'red':18, 'green':23, 'blue':24})

    # Simulate button press triggering photo capture
    blm.handle_button_press = MagicMock()
    blm._on_button_press(channel=17)
    blm.handle_button_press.assert_called_once()
