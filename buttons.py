from gpiozero import Button
import yaml

cfg = yaml.safe_load(open("config.yaml"))
btn = Button(cfg["gpio"]["button"], hold_time=2)
