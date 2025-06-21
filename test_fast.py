# test_display.py
from display_fast import show_on_inky
import time
import os

# Ajuste: substitua pelo nome de um ficheiro real em ./images/
IMAGE_DIR = './images'
backgrounds = [f for f in os.listdir(IMAGE_DIR) if f.endswith('.png')]
if not backgrounds:
    print('Nenhuma imagem encontrada em ./images')
    exit(1)

# Mostra a primeira imagem e aguarda 5 segundos
bg = os.path.join(IMAGE_DIR, backgrounds[0])
print(f'Mostrando {bg} no Inky...')
show_on_inky(
    bg,
    photos_taken=10,
    gifs_created=5,
    battery_level=75,
    wifi_strength=True,
    state_text='TESTE',
    show_camera_icon=True,
    show_gif_icon=True,
    show_error_icon=False
)
# Mantém o display ligado antes de sair
print('Imagem mostrada. Aguardar 10 segundos antes de sair...')
time.sleep(10)
print('Fim do teste')

