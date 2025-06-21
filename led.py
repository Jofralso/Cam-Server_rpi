import yaml
from gpiozero import LED
from gpiozero.pins.rpigpio import RPiGPIOFactory
import time

cfg = yaml.safe_load(open("config.yaml"))
factory = RPiGPIOFactory()
led_red = LED(cfg["gpio"]["led_red"], pin_factory=factory)
led_green = LED(cfg["gpio"]["led_green"], pin_factory=factory)
led_blue = LED(cfg["gpio"]["led_blue"], pin_factory=factory)

def indicate(action):
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
