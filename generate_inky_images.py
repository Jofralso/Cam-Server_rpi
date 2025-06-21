
from PIL import Image, ImageDraw, ImageFont
import os

# Inky pHAT dimensions
WIDTH = 190  # Ajustado no teu script, podes corrigir para 212 se quiseres
HEIGHT = 94

# Cores (preto, vermelho, branco)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Fonte para texto
try:
    font = ImageFont.truetype("DejaVuSansMono-Bold.ttf", 10)
except IOError:
    font = ImageFont.load_default()

def create_rounded_rect_mask(size, radius):
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, size[0], size[1]), radius=radius, fill=255)
    return mask

def draw_battery_icon(draw, x, y, level, color=BLACK):
    draw.rectangle((x, y + 2, x + 18, y + 8), outline=color)
    draw.rectangle((x + 19, y + 4, x + 20, y + 6), fill=color)
    fill_width = int(16 * (level / 100.0))
    draw.rectangle((x + 1, y + 3, x + 1 + fill_width, y + 7), fill=color)

def draw_wifi_icon(draw, x, y, color=BLACK):
    draw.arc((x, y + 8, x + 10, y + 10), 180, 0, fill=color)
    draw.arc((x - 2, y + 4, x + 12, y + 12), 180, 0, fill=color)
    draw.arc((x - 4, y, x + 14, y + 14), 180, 0, fill=color)
    draw.ellipse((x + 4, y + 12, x + 6, y + 14), fill=color)

def draw_camera_icon(draw, x, y, color=BLACK):
    draw.rectangle((x, y + 4, x + 12, y + 12), outline=color)
    draw.rectangle((x + 2, y, x + 10, y + 4), outline=color)
    draw.ellipse((x + 3, y + 5, x + 9, y + 11), outline=color)
    draw.ellipse((x + 5, y + 7, x + 7, y + 9), fill=color)

def draw_gif_icon(draw, x, y, color=BLACK):
    draw.text((x, y), "GIF", font=font, fill=color)

def draw_error_icon(draw, x, y, color=RED):
    draw.ellipse((x, y, x + 12, y + 12), outline=color)
    draw.line((x + 6, y + 2, x + 6, y + 8), fill=color, width=2)
    draw.line((x + 6, y + 10, x + 6, y + 10), fill=color, width=2)

def convert_to_inky_palette(img):
    # Paleta com as cores do Inky: branco, preto, vermelho
    palette = [
        255, 255, 255,  # Branco
        0, 0, 0,        # Preto
        255, 0, 0       # Vermelho
    ] + [0, 0, 0] * 253  # completar 256 cores

    paletted = Image.new("P", img.size)
    paletted.putpalette(palette)

    img = img.convert("RGB")
    img_quant = img.quantize(palette=paletted)

    return img_quant

def create_inky_image(background_path, output_filename, photos_taken=None, gifs_created=None,
                      battery_level=None, wifi_strength=None, state_text=None,
                      show_camera_icon=False, show_gif_icon=False, show_error_icon=False):
    try:
        original_background = Image.open(background_path).convert("RGB")
    except FileNotFoundError:
        print(f"Erro: Imagem de fundo não encontrada em {background_path}")
        return

    img = Image.new("RGB", (WIDTH, HEIGHT), WHITE)
    draw = ImageDraw.Draw(img)

    image_padding = 25
    image_section_width = WIDTH // 2

    original_width, original_height = original_background.size
    aspect_ratio = original_width / original_height

    new_height = HEIGHT
    new_width = int(new_height * aspect_ratio)
    if new_width > image_section_width:
        new_width = image_section_width
        new_height = int(new_width / aspect_ratio)

    resized_background = original_background.resize((new_width, new_height), Image.LANCZOS)

    paste_x = image_padding + ((image_section_width - (2 * image_padding)) - new_width) // 2
    paste_y = (HEIGHT - new_height) // 2
    img.paste(resized_background, (paste_x, paste_y))

    text_section_start_x = image_section_width
    text_x_offset = text_section_start_x + 5

    current_y = 5
    if battery_level is not None:
        draw_battery_icon(draw, text_x_offset, current_y, battery_level)
        current_y += 15

    if wifi_strength is not None:
        draw_wifi_icon(draw, text_x_offset, current_y)
        current_y += 15

    current_y = 5
    if photos_taken is not None:
        draw.text((text_x_offset + 40, current_y), f"P:{photos_taken}", font=font, fill=BLACK)
        current_y += 15

    if gifs_created is not None:
        draw.text((text_x_offset + 40, current_y), f"G:{gifs_created}", font=font, fill=BLACK)
        current_y += 15

    if state_text:
        draw.text((text_x_offset, HEIGHT - 15), state_text, font=font, fill=BLACK)

    icon_y_br = HEIGHT - 20
    icon_x_br = WIDTH - 20

    if show_camera_icon:
        draw_camera_icon(draw, icon_x_br, icon_y_br)
    if show_gif_icon:
        draw_gif_icon(draw, icon_x_br - 10, icon_y_br)
    if show_error_icon:
        draw_error_icon(draw, icon_x_br, icon_y_br)

    # Remove a máscara alpha para evitar problemas no Inky, pois ele não suporta transparência
    # Aplica a conversão para paleta 3 cores antes de salvar
    img_inky = convert_to_inky_palette(img)
    img_inky.save(output_filename)
    print(f"Imagem gerada: {output_filename}")

# Define paths
IMAGE_DIR = "./images/"
OUTPUT_DIR = "./output/"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Exemplos de uso (igual ao teu original)
create_inky_image(
    os.path.join(IMAGE_DIR, "apple_mascot_ligado.png"),
    os.path.join(OUTPUT_DIR, "inky_ligado.png"),
    photos_taken=123,
    gifs_created=45,
    battery_level=80,
    wifi_strength=True,
    state_text="LIGADO"
)

create_inky_image(
    os.path.join(IMAGE_DIR, "apple_mascot_standby.png"),
    os.path.join(OUTPUT_DIR, "inky_standby.png"),
    photos_taken=123,
    gifs_created=45,
    battery_level=60,
    wifi_strength=True,
    state_text="STANDBY"
)

create_inky_image(
    os.path.join(IMAGE_DIR, "apple_mascot_desligado.png"),
    os.path.join(OUTPUT_DIR, "inky_desligado.png"),
    state_text="DESLIGADO"
)

create_inky_image(
    os.path.join(IMAGE_DIR, "apple_mascot_tirar_foto.png"),
    os.path.join(OUTPUT_DIR, "inky_tirar_foto.png"),
    photos_taken=124,
    gifs_created=45,
    battery_level=75,
    wifi_strength=True,
    state_text="A TIRAR FOTO",
    show_camera_icon=True
)

create_inky_image(
    os.path.join(IMAGE_DIR, "apple_mascot_tirar_gif.png"),
    os.path.join(OUTPUT_DIR, "inky_tirar_gif.png"),
    photos_taken=124,
    gifs_created=46,
    battery_level=70,
    wifi_strength=True,
    state_text="A TIRAR GIF",
    show_gif_icon=True
)

create_inky_image(
    os.path.join(IMAGE_DIR, "apple_mascot_erro.png"),
    os.path.join(OUTPUT_DIR, "inky_erro.png"),
    photos_taken=123,
    gifs_created=45,
    battery_level=50,
    wifi_strength=False,
    state_text="ERRO",
    show_error_icon=True
)
