import yaml
from gpiozero import LED
from gpiozero.pins.rpigpio import RPiGPIOFactory
import time
import logging

# Add proper error handling for GPIO initialization
try:
    cfg = yaml.safe_load(open("config.yaml"))
    factory = RPiGPIOFactory()
    
    # Get LED pin numbers from config
    led_red_pin = cfg["gpio"]["led"]["red"]
    led_green_pin = cfg["gpio"]["led"]["green"]
    led_blue_pin = cfg["gpio"]["led"]["blue"]
    
    # Initialize LEDs with proper error handling
    try:
        led_red = LED(led_red_pin, pin_factory=factory)
        led_green = LED(led_green_pin, pin_factory=factory)
        led_blue = LED(led_blue_pin, pin_factory=factory)
        
        # Make sure LEDs are off initially
        led_red.off()
        led_green.off()
        led_blue.off()
        
        led_initialized = True
    except Exception as e:
        logging.error(f"Failed to initialize LED hardware: {e}")
        # Create dummy LED objects for graceful degradation
        led_initialized = False
        
        # Define dummy LED class with same interface but does nothing
        class DummyLED:
            def on(self): pass
            def off(self): pass
            def blink(self, on_time=1, off_time=1, n=None): pass
        
        led_red = DummyLED()
        led_green = DummyLED()
        led_blue = DummyLED()
        
except Exception as e:
    logging.error(f"Error loading config or initializing GPIO: {e}")
    led_initialized = False
    
    # Define dummy LED class
    class DummyLED:
        def on(self): pass
        def off(self): pass
        def blink(self, on_time=1, off_time=1, n=None): pass
    
    led_red = DummyLED()
    led_green = DummyLED()
    led_blue = DummyLED()

def indicate(action):
    if not led_initialized:
        logging.warning(f"LED action '{action}' skipped - LEDs not initialized")
        return
        
    if action == "ready":
        led_green.on()
        led_red.off()
        led_blue.off()
    elif action == "photo":
        led_blue.blink(on_time=0.2, off_time=0.2, n=3)
    elif action == "gif":
        led_red.blink(on_time=0.1, off_time=0.1, n=5)
    elif action == "off":
        led_red.off()
        led_green.off()
        led_blue.off()
