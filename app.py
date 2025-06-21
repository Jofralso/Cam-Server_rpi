import yaml
from flask import Flask, render_template, send_from_directory, jsonify, request
from pathlib import Path
from threading import Thread
from scripts.capture import capture_photo, capture_gif
from display_fast import show_on_inky
from led import indicate
from buttons import btn
import time
import logging



logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# Load config
cfg_path = Path('config.yaml')
cfg = yaml.safe_load(cfg_path.read_text())

photo_dir = Path(cfg['paths']['photos'])
photo_dir.mkdir(exist_ok=True)

counter = {'photos': 0, 'gifs': 0}

app = Flask(__name__)

def update_display(state_text="", show_camera_icon=False, show_gif_icon=False, show_error_icon=False):
    mascot_base = cfg['inky']['mascot']
    img_path = f"./images/{mascot_base}.png"

    try:
        show_on_inky(
            img_path,
            photos_taken=counter['photos'],
            gifs_created=counter['gifs'],
            battery_level=None,
            wifi_strength=None,
            state_text=state_text,
            show_camera_icon=show_camera_icon,
            show_gif_icon=show_gif_icon,
            show_error_icon=show_error_icon,
        )
        logging.info(f"Atualizando display: mascote {mascot_base} - estado '{state_text}'")
    except FileNotFoundError:
        logging.error(f"Erro: Imagem de fundo não encontrada em {img_path}")

@app.route('/')
def index():
    # Listar imagens fotos e gifs para galeria
    items = sorted(photo_dir.iterdir(), reverse=True)
    photos = [p.name for p in items if p.suffix.lower() in ['.jpg', '.jpeg', '.png']]
    gifs = [p.name for p in items if p.suffix.lower() == '.gif']
    return render_template('index.html', photos=photos, gifs=gifs, mascot=cfg['inky']['mascot'])

@app.route('/photos/<name>')
def photo(name):
    # Serve fotos/gifs da pasta
    return send_from_directory(str(photo_dir), name)

@app.route('/api/status')
def status():
    return jsonify(counter)

@app.route('/api/button_press', methods=['POST'])
def button_press():
    data = request.json or {}
    t = data.get('type')
    logging.info(f"Button pressed of type: {t}")

    if t == 'photo':
        counter['photos'] += 1
        indicate('photo')
        update_display(state_text='A TIRAR FOTO', show_camera_icon=True)
        capture_photo()
        update_display(state_text='Pronto')
    elif t == 'gif':
        counter['gifs'] += 1
        indicate('gif')
        update_display(state_text='A TIRAR GIF', show_gif_icon=True)
        capture_gif()
        update_display(state_text='Pronto')
    else:
        logging.warning(f"Tipo de botão desconhecido: {t}")

    return jsonify(result='ok')

@app.route('/api/toggle_mascot', methods=['POST'])
def toggle_mascot():
    mascots = cfg['inky'].get('available_mascots', [])
    current = cfg['inky'].get('mascot', '')

    if not mascots:
        return jsonify({'error': 'Nenhuma mascote configurada'}), 500

    try:
        idx = mascots.index(current)
        new_mascot = mascots[(idx + 1) % len(mascots)]
    except ValueError:
        new_mascot = mascots[0]

    cfg['inky']['mascot'] = new_mascot
    cfg_path.write_text(yaml.safe_dump(cfg))

    update_display(state_text=f'Mascote: {new_mascot.replace("_", " ").title()}')

    logging.info(f"Mascote alternada para: {new_mascot}")
    return jsonify({'current_mascot': new_mascot})

def handle_button():
    def on_press():
        logging.info("Physical button pressed: take photo")
        counter['photos'] += 1
        indicate('photo')
        update_display(state_text='A TIRAR FOTO', show_camera_icon=True)
        capture_photo()
        update_display(state_text='Pronto')

    def on_hold():
        logging.info("Physical button held: take gif")
        counter['gifs'] += 1
        indicate('gif')
        update_display(state_text='A TIRAR GIF', show_gif_icon=True)
        capture_gif()
        update_display(state_text='Pronto')

    btn.when_pressed = on_press
    btn.when_held = on_hold

if __name__ == '__main__':
    logging.info("Starting app...")
    indicate('ready')
    update_display(state_text='Servidor ON')
    handle_button()

    flask_thread = Thread(target=lambda: app.run(host='0.0.0.0', port=8000, debug=False, use_reloader=False))
    flask_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Stopping app...")
        indicate('off')
