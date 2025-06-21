#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

# Button pin
BUTTON_PIN = 5  # GPIO5

# Configure GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Use internal pull-up

def button_callback(channel):
    if GPIO.input(BUTTON_PIN):
        logging.info("Button RELEASED")
    else:
        logging.info("Button PRESSED!")

try:
    # Add event detection for both rising and falling edges
    GPIO.add_event_detect(BUTTON_PIN, GPIO.BOTH, callback=button_callback, bouncetime=200)
    
    logging.info(f"Button test started on GPIO{BUTTON_PIN}")
    logging.info("Press the button to test (Ctrl+C to exit)...")
    
    # Simple counter to track presses
    presses = 0
    
    # Main loop
    while True:
        # Check if button is pressed (LOW because button connects to GND)
        if not GPIO.input(BUTTON_PIN):
            presses += 1
            logging.info(f"Button press detected! (Press #{presses})")
            
            # Wait for release to avoid counting multiple times
            while not GPIO.input(BUTTON_PIN):
                time.sleep(0.1)
                
            logging.info("Button released")
        
        time.sleep(0.1)  # Slight delay to reduce CPU usage

except KeyboardInterrupt:
    logging.info("Test stopped by user")
finally:
    # Clean up GPIO
    GPIO.cleanup()
    logging.info("GPIO cleaned up")
