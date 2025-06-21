import yaml
from flask import Flask, render_template, send_from_directory, jsonify, request
from pathlib import Path
from threading import Thread
from scripts.capture import capture_photo, capture_gif
from display import show_on_inky
from led import indicate
from buttons import btn
import time
import logging
import threading



logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# Load config
cfg_path = Path('config.yaml')
cfg = yaml.safe_load(cfg_path.read_text())

photo_dir = Path(cfg['paths']['photos'])
photo_dir.mkdir(exist_ok=True)

counter = {'photos': 0, 'gifs': 0}

# Track when the last photo/gif was taken
last_capture_time = 0

# Inicializar contador com arquivos existentes
def initialize_counters():
    global counter
    photo_files = [p for p in photo_dir.iterdir() if p.suffix.lower() in ['.jpg', '.jpeg', '.png']]
    gif_files = [p for p in photo_dir.iterdir() if p.suffix.lower() == '.gif']
    counter['photos'] = len(photo_files)
    counter['gifs'] = len(gif_files)
    logging.info(f"Contadores inicializados: {len(photo_files)} fotos, {len(gif_files)} GIFs encontrados")

# Inicializar contadores com arquivos existentes
initialize_counters()

app = Flask(__name__)

def update_display(state_text="", show_camera_icon=False, show_gif_icon=False, show_error_icon=False):
    # Build path from theme and state
    theme = cfg['inky']['current_theme']
    state = cfg['inky']['current_state']
    mascot_id = f"{theme}_{state}"
    img_path = f"./images/{mascot_id}.png"

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
        logging.info(f"Atualizando display: mascote {mascot_id} - estado '{state_text}'")
    except FileNotFoundError:
        logging.error(f"Erro: Imagem de fundo não encontrada em {img_path}")

@app.route('/')
def index():
    # Listar imagens fotos e gifs para galeria
    items = sorted(photo_dir.iterdir(), reverse=True)
    photos = [p.name for p in items if p.suffix.lower() in ['.jpg', '.jpeg', '.png']]
    gifs = [p.name for p in items if p.suffix.lower() == '.gif']
    
    # Use current_theme instead of mascot
    theme = cfg['inky']['current_theme']
    state = cfg['inky']['current_state']
    mascot_id = f"{theme}_{state}"
    
    return render_template('index.html', photos=photos, gifs=gifs, mascot=mascot_id)

@app.route('/photos/<name>')
def photo(name):
    # Serve fotos/gifs da pasta
    return send_from_directory(str(photo_dir), name)

@app.route('/api/status')
def status():
    return jsonify(counter)

@app.route('/api/last_capture')
def last_capture():
    return jsonify({'timestamp': last_capture_time})

@app.route('/api/button_press', methods=['POST'])
def button_press():
    global last_capture_time
    data = request.json or {}
    t = data.get('type')
    logging.info(f"Button pressed of type: {t}")

    if t == 'photo':
        counter['photos'] += 1
        indicate('photo')
        
        # Set state to photo mode
        cfg['inky']['current_state'] = 'tirar_foto'
        cfg_path.write_text(yaml.safe_dump(cfg))
        
        update_display(state_text='A TIRAR FOTO', show_camera_icon=True)
        capture_photo()
        
        # Update timestamp for auto-refresh
        last_capture_time = time.time()
        
        # Start standby timer to reset display after 30 seconds
        start_standby_timer()
    elif t == 'gif':
        counter['gifs'] += 1
        indicate('gif')
        
        # Set state to gif mode
        cfg['inky']['current_state'] = 'tirar_gif'
        cfg_path.write_text(yaml.safe_dump(cfg))
        
        update_display(state_text='A TIRAR GIF', show_gif_icon=True)
        capture_gif()
        
        # Update timestamp for auto-refresh
        last_capture_time = time.time()
        
        # Start standby timer to reset display after 30 seconds
        start_standby_timer()
    else:
        logging.warning(f"Tipo de botão desconhecido: {t}")

    return jsonify(result='ok')

@app.route('/api/toggle_mascot', methods=['POST'])
def toggle_mascot():
    # Toggle between themes
    current_theme = cfg['inky']['current_theme']
    
    # Simple toggle between two themes
    new_theme = "apple_mascot" if current_theme == "steve_jobs" else "steve_jobs"
    
    # Update theme in config
    cfg['inky']['current_theme'] = new_theme
    cfg_path.write_text(yaml.safe_dump(cfg))
    
    # Show the change on display
    update_display(state_text=f'Tema: {new_theme.replace("_", " ").title()}')
    
    logging.info(f"Mascote alternada para tema: {new_theme}")
    return jsonify({'current_theme': new_theme})

def handle_button():
    def on_press():
        global last_capture_time
        logging.info("Physical button pressed: take photo")
        counter['photos'] += 1
        indicate('photo')
        
        # Set state to photo mode
        cfg['inky']['current_state'] = 'tirar_foto'
        cfg_path.write_text(yaml.safe_dump(cfg))
        
        update_display(state_text='A TIRAR FOTO', show_camera_icon=True)
        capture_photo()
        
        # Update timestamp for auto-refresh
        last_capture_time = time.time()
        
        # Start standby timer
        start_standby_timer()

    def on_hold():
        global last_capture_time
        logging.info("Physical button held: take gif")
        counter['gifs'] += 1
        indicate('gif')
        
        # Set state to gif mode
        cfg['inky']['current_state'] = 'tirar_gif'
        cfg_path.write_text(yaml.safe_dump(cfg))
        
        update_display(state_text='A TIRAR GIF', show_gif_icon=True)
        capture_gif()
        
        # Update timestamp for auto-refresh
        last_capture_time = time.time()
        
        # Start standby timer
        start_standby_timer()

    btn.when_pressed = on_press
    btn.when_held = on_hold

# Add below the imports at the top of the file
import threading
import time

# Add these global variables for state management
display_timer = None
display_lock = threading.Lock()

# Add these functions to handle display state timeout
def reset_to_standby():
    """Reset display to standby state after timeout"""
    with display_lock:
        # Change state to standby in config
        cfg['inky']['current_state'] = 'standby'
        cfg_path.write_text(yaml.safe_dump(cfg))
        # Update display with standby state
        update_display(state_text='Standby')
        logging.info("Auto-reset display to standby state")

def start_standby_timer():
    """Start a timer to reset display to standby after 30 seconds"""
    global display_timer
    # Cancel any existing timer
    if display_timer:
        display_timer.cancel()
    
    # Create new timer
    display_timer = threading.Timer(30.0, reset_to_standby)
    display_timer.daemon = True
    display_timer.start()
    logging.info("Standby timer started (30s)")

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
