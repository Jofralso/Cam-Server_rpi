import yaml
from gpiozero import Button
from gpiozero.pins.rpigpio import RPiGPIOFactory

cfg = yaml.safe_load(open("config.yaml"))
factory = RPiGPIOFactory()
btn = Button(pin=cfg["gpio"]["button"], hold_time=2, pin_factory=factory)
