import yaml
import time
import threading
import logging
from gpiozero import RGBLED
from gpiozero.pins.rpigpio import RPiGPIOFactory

# Load config
try:
    cfg = yaml.safe_load(open('config.yaml'))
    LED_RED = cfg['gpio']['led']['red']
    LED_GREEN = cfg['gpio']['led']['green']
    LED_BLUE = cfg['gpio']['led']['blue']
except Exception as e:
    logging.error(f"Error loading LED config: {e}")
    # Default pins if config fails
    LED_RED = 20
    LED_GREEN = 21
    LED_BLUE = 16

# Create RGB LED object
try:
    factory = RPiGPIOFactory()
    led = RGBLED(red=LED_RED, green=LED_GREEN, blue=LED_BLUE, pin_factory=factory)
    led_enabled = True
    logging.info(f"LED initialized on GPIO R:{LED_RED} G:{LED_GREEN} B:{LED_BLUE}")
except Exception as e:
    led_enabled = False
    logging.error(f"Failed to initialize LED: {e}")

# Define colors
WHITE = (1, 1, 1)
RED = (1, 0, 0)
GREEN = (0, 1, 0)
BLUE = (0, 0, 1)
YELLOW = (1, 1, 0)
OFF = (0, 0, 0)

# Keep track of flashing threads
flash_thread = None
flash_stop_event = threading.Event()

def stop_flashing():
    """Stop any ongoing flashing"""
    global flash_thread, flash_stop_event
    if flash_thread and flash_thread.is_alive():
        flash_stop_event.set()
        flash_thread.join(1)  # Wait for thread to finish
        flash_stop_event.clear()

def flash_led(color, duration=3, interval=0.2):
    """Flash LED in specified color for duration"""
    if not led_enabled:
        return

    def _flash_task():
        end_time = time.time() + duration
        while time.time() < end_time and not flash_stop_event.is_set():
            led.color = color
            flash_stop_event.wait(interval)
            if flash_stop_event.is_set():
                break
            led.color = OFF
            flash_stop_event.wait(interval)
            if flash_stop_event.is_set():
                break
        
        # Return to WHITE after flashing (if not stopped)
        if not flash_stop_event.is_set():
            led.color = GREEN

    stop_flashing()  # Stop any existing flashing
    global flash_thread
    flash_thread = threading.Thread(target=_flash_task)
    flash_thread.daemon = True
    flash_thread.start()

def set_color(color, duration=None):
    """Set LED to solid color, optionally for a duration"""
    if not led_enabled:
        return
    
    stop_flashing()  # Stop any existing flashing
    led.color = color
    
    if duration:
        # Return to WHITE after duration
        def _reset():
            time.sleep(duration)
            if led_enabled:
                led.color = WHITE
        
        thread = threading.Thread(target=_reset)
        thread.daemon = True
        thread.start()

def indicate(state):
    """Set LED based on camera state"""
    if state == 'ready' or state == 'on':
        set_color(GREEN)  # White when on/ready
    elif state == 'photo':
        flash_led(GREEN, duration=3, interval=0.2)  # Flash green for 3 seconds
    elif state == 'gif':
        flash_led(BLUE, duration=3, interval=0.2)  # Solid blue for 3 seconds
    elif state == 'error':
        flash_led(RED, duration=3, interval=0.1)  # Fast flash red for errors
    elif state == 'off':
        set_color(OFF)  # Turn off LED
    else:
        set_color(GREEN)  # Default to white
