from PIL import Image, ImageDraw, ImageFont
import numpy as np
from inky import auto

# Inicializa o driver inky
inky = auto()
WIDTH, HEIGHT = inky.width, inky.height
inky.set_border(inky.WHITE)

# Cores para o inky standard
WHITE = inky.WHITE
BLACK = inky.BLACK
RED = inky.RED if hasattr(inky, 'RED') else inky.BLACK

# Carrega fonte maior
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 18)
except IOError:
    font = ImageFont.load_default()

def draw_camera_icon(draw, x, y, color=BLACK):
    draw.rectangle((x, y + 4, x + 12, y + 12), outline=color)
    draw.rectangle((x + 2, y, x + 10, y + 4), outline=color)
    draw.ellipse((x + 3, y + 5, x + 9, y + 11), outline=color)
    draw.ellipse((x + 5, y + 7, x + 7, y + 9), fill=color)

def draw_gif_icon(draw, x, y, color=BLACK):
    draw.text((x, y), "GIF", font=font, fill=color)

def draw_error_icon(draw, x, y, color=BLACK):
    draw.ellipse((x, y, x + 12, y + 12), outline=color)
    draw.line((x + 6, y + 2, x + 6, y + 8), fill=color, width=2)
    draw.line((x + 6, y + 10, x + 6, y + 10), fill=color, width=2)

def show_on_inky(background_path,
                 photos_taken=None,
                 gifs_created=None,
                 battery_level=None,
                 wifi_strength=None,
                 state_text=None,
                 show_camera_icon=False,
                 show_gif_icon=False,
                 show_error_icon=False):
    # 1) Abre imagem de fundo e converte para grayscale
    try:
        bg = Image.open(background_path).convert("L")
    except FileNotFoundError:
        print(f"Erro: Imagem de fundo não encontrada em {background_path}")
        return
    except Exception as e:
        print(f"Erro ao abrir imagem: {e}")
        return

    # 2) Cria canvas com paleta para o inky
    img = Image.new("P", (WIDTH, HEIGHT))
    img.putpalette([255, 255, 255, 0, 0, 0, 255, 0, 0])
    img.paste(WHITE, (0, 0, WIDTH, HEIGHT))
    draw = ImageDraw.Draw(img)

    # 3) Cola o bg na metade esquerda, mantendo proporção
    if bg:
        section_w = WIDTH // 2
        padding = 20
        ow, oh = bg.size
        ar = ow / oh
        nh = HEIGHT
        nw = int(nh * ar)
        if nw > section_w - 2 * padding:
            nw = section_w - 2 * padding
            nh = int(nw / ar)
        bg_r = bg.resize((nw, nh), Image.LANCZOS)
        px = padding + (section_w - 2 * padding - nw) // 2
        py = (HEIGHT - nh) // 2
        
        # Convert to 1-bit and paste with the correct color
        bw_bg = bg_r.point(lambda x: WHITE if x > 128 else BLACK)
        img.paste(bw_bg, (px, py))

    # 4) Desenha texto em preto na metade direita
    tx, ty = WIDTH // 2 + 5, 5
    if photos_taken is not None:
        draw.text((tx, ty), f"Fotos: {photos_taken}", font=font, fill=BLACK)
        ty += 30
    if gifs_created is not None:
        draw.text((tx, ty), f"GIFs: {gifs_created}", font=font, fill=BLACK)
        ty += 30
    if battery_level is not None:
        draw.text((tx, ty), f"Bateria: {battery_level}%", font=font, fill=BLACK)
        ty += 30
    if wifi_strength is not None:
        draw.text((tx, ty), f"WIFI: {'Sim' if wifi_strength else 'Não'}", font=font, fill=BLACK)
        ty += 30
    if state_text:
        draw.text((tx, HEIGHT - 35), state_text, font=font, fill=BLACK)

    # 5) Ícones no canto inferior direito
    ix, iy = WIDTH - 20, HEIGHT - 40
    if show_error_icon:
        draw_error_icon(draw, ix, iy)
        ix -= 20
    if show_gif_icon:
        draw_gif_icon(draw, ix - 20, iy)
        ix -= 40
    if show_camera_icon:
        draw_camera_icon(draw, ix - 20, iy)

    # 6) Envia para o inky e atualiza o e-paper
    inky.set_image(img)
    inky.show()

# Function that app.py actually calls
def update_display(state_text='standby', counter=None, show_camera_icon=False, 
                   show_gif_icon=False, show_error_icon=False):
    # Get mascot from config
    import yaml
    from pathlib import Path
    
    try:
        cfg_path = Path('config.yaml')
        cfg = yaml.safe_load(cfg_path.read_text())
        mascot_path = f"static/mascots/{cfg['inky']['mascot']}.png"
        
        # Pass all data to show_on_inky function
        photos_taken = counter['photos'] if counter else None
        gifs_created = counter['gifs'] if counter else None
        
        show_on_inky(
            background_path=mascot_path,
            photos_taken=photos_taken,
            gifs_created=gifs_created,
            state_text=state_text,
            show_camera_icon=show_camera_icon,
            show_gif_icon=show_gif_icon,
            show_error_icon=show_error_icon
        )
    except Exception as e:
        print(f"Erro ao atualizar display: {e}")
