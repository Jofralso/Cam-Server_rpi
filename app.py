import yaml
from flask import Flask, render_template, send_from_directory, jsonify
from scripts.capture import capture_photo, capture_gif
from display import show_status
from led import indicate
from buttons import btn
from threading import Thread
from pathlib import Path
import time

cfg = yaml.safe_load(open("config.yaml"))
photo_dir = Path(cfg["paths"]["photos"])
photo_dir.mkdir(exist_ok=True)

app = Flask(__name__)
counter = {"photos":0, "gifs":0}

@app.route("/")
def index():
    items = sorted(photo_dir.iterdir(), reverse=True)
    return render_template("index.html", items=[p.name for p in items])

@app.route("/photos/<name>")
def photo(name):
    return send_from_directory(photo_dir, name)

@app.route("/api/status")
def status():
    return jsonify(counter)

def handle_button():
    def on_press():
        counter["photos"] += 1
        indicate("photo")
        capture_photo()
        show_status("Foto", counter["photos"])
    def on_hold():
        counter["gifs"] += 1
        indicate("gif")
        capture_gif()
        show_status("GIF!", counter["gifs"])
    btn.when_pressed = on_press
    btn.when_held = on_hold

if __name__ == "__main__":
    indicate("ready")
    show_status("Servidor ON", 0)
    handle_button()
    th = Thread(target=lambda: app.run(host="0.0.0.0", port=8000))
    th.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        indicate("off")
