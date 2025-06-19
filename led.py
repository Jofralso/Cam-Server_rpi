from gpiozero import RGBLED
import yaml

cfg = yaml.safe_load(open("config.yaml"))
gp = cfg["gpio"]
led = RGBLED(int(gp["led_red"]), int(gp["led_green"]), int(gp["led_blue"]))

def indicate(state):
    palette = {
        "ready": (0,1,0),
        "photo": (1,1,0),
        "gif": (0,0,1),
        "off": (1,0,0),
    }
    led.color = palette.get(state, (0,0,0))
