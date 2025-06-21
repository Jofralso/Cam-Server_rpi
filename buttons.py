import yaml
from gpiozero import Button
from gpiozero.pins.rpigpio import RPiGPIOFactory
import logging

try:
    # Try some alternative pins that shouldn't conflict with Inky
    SAFE_PINS = [6]
    
    cfg = yaml.safe_load(open("config.yaml"))
    factory = RPiGPIOFactory()
    
    # Find a usable pin
    button_initialized = False
    used_pin = None
    
    for pin_num in SAFE_PINS:
        try:
            btn = Button(pin=pin_num, hold_time=2, pin_factory=factory)
            button_initialized = True
            used_pin = pin_num
            logging.info(f"Button initialized on GPIO {pin_num}")
            
            # Update config with working pin
            if cfg["gpio"]["button"] != pin_num:
                cfg["gpio"]["button"] = pin_num
                with open("config.yaml", 'w') as f:
                    yaml.dump(cfg, f)
                logging.info(f"Updated button pin in config to GPIO {pin_num}")
            break
        except Exception as e:
            logging.warning(f"Could not use GPIO {pin_num}: {e}")
            continue
    
    if not button_initialized:
        logging.error("Failed to initialize button on any available GPIO pin")
        # Create dummy button
        class DummyButton:
            def __init__(self):
                self.when_pressed = None
                self.when_held = None
                self.when_released = None
        
        btn = DummyButton()
        
except Exception as e:
    logging.error(f"Error initializing button: {e}")
    
    # Create dummy button
    class DummyButton:
        def __init__(self):
            self.when_pressed = None
            self.when_held = None
            self.when_released = None
    
    btn = DummyButton()
    button_initialized = False
