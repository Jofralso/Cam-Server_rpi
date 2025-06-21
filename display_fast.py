from PIL import Image, ImageDraw, ImageFont
from inky_fast.inky_fast import InkyFast
import numpy as np
import os

# Inicializa o driver rápido do Inky diretamente com resolução do hardware
inky = InkyFast(resolution=(250, 122), colour="red")
WIDTH, HEIGHT = inky.width, inky.height
inky.set_border(WHITE)

# Cores no buffer: WHITE=0, BLACK=1, RED=2
WHITE = 0
BLACK = 1
RED = 2

# Carrega fonte maior
try:
    font = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 18
    )
except IOError:
    font = ImageFont.load_default()

# Ícones
def draw_camera_icon(draw, x, y, color=BLACK):
    draw.rectangle((x, y+4, x+12, y+12), outline=color)
    draw.rectangle((x+2, y, x+10, y+4), outline=color)
    draw.ellipse((x+3, y+5, x+9, y+11), outline=color)
    draw.ellipse((x+5, y+7, x+7, y+9), fill=color)

def draw_gif_icon(draw, x, y, color=BLACK):
    draw.text((x, y), "GIF", font=font, fill=color)

def draw_error_icon(draw, x, y, color=BLACK):
    draw.ellipse((x, y, x+12, y+12), outline=color)
    draw.line((x+6, y+2, x+6, y+8), fill=color, width=2)
    draw.line((x+6, y+10, x+6, y+10), fill=color, width=2)

# Função principal de exibição
def show_on_inky(
    background_path,
    photos_taken=None,
    gifs_created=None,
    battery_level=None,
    wifi_strength=None,
    state_text=None,
    show_camera_icon=False,
    show_gif_icon=False,
    show_error_icon=False,
):
    # 1) Abre imagem de fundo e converte para grayscale
    if not os.path.exists(background_path):
        print(f"Erro: Imagem de fundo não encontrada em {background_path}")
        return
    bg = Image.open(background_path).convert("L")

    # 2) Cria canvas grayscale (L) com fundo branco (255)
    canvas = Image.new("L", (WIDTH, HEIGHT), 255)
    draw = ImageDraw.Draw(canvas)

    # 3) Cola o bg na metade esquerda, mantendo proporção
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
    canvas.paste(bg_r, (px, py))

    # 4) Desenha texto em preto (0) na metade direita
    tx, ty = section_w + 5, 5
    if photos_taken is not None:
        draw.text((tx, ty), f"Fotos: {photos_taken}", font=font, fill=0)
        ty += 30
    if gifs_created is not None:
        draw.text((tx, ty), f"GIFs: {gifs_created}", font=font, fill=0)
        ty += 30
    if battery_level is not None:
        draw.text((tx, ty), f"Bateria: {battery_level}%", font=font, fill=0)
        ty += 30
    if wifi_strength is not None:
        draw.text((tx, ty), f"WIFI: {'Sim' if wifi_strength else 'Não'}", font=font, fill=0)
        ty += 30
    if state_text:
        draw.text((tx, HEIGHT - 35), state_text, font=font, fill=0)

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

    # 6) Converte para bitmap 1-bit (pil mode '1')
    bw = canvas.point(lambda x: 0 if x < 128 else 1, '1')

    # 7) Transforma em numpy array e reshape para (HEIGHT, WIDTH)
    arr = np.array(bw, dtype=np.uint8).reshape((HEIGHT, WIDTH))

    # 8) Envia para InkyFast e atualiza rapidamente
    inky.set_image(arr)
    inky.show_stay_awake()

# Test harness
if __name__ == '__main__':
    import tempfile
    from PIL import Image

    tmp = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    img = Image.new('RGB', (100, 100), (255, 0, 0))
    img.save(tmp.name)

    print('Testing show_on_inky with dummy image and parameters...')
    def dummy_set_image(buffer):
        print('Buffer shape:', buffer.shape)
        assert buffer.shape == (HEIGHT, WIDTH), 'Buffer shape mismatch'
    inky.set_image = dummy_set_image

    show_on_inky(
        tmp.name,
        photos_taken=1,
        gifs_created=2,
        battery_level=50,
        wifi_strength=True,
        state_text='TEST',
        show_camera_icon=True,
        show_gif_icon=True,
        show_error_icon=True
    )
    print('Test passed')
    tmp.close()
