from inky.auto import auto
from PIL import Image, ImageFont, ImageDraw
from pathlib import Path

inky = auto()
font = ImageFont.load_default()

def show_status(msg, count):
    img = Image.new("P", (inky.WIDTH, inky.HEIGHT), color=inky.WHITE)
    d = ImageDraw.Draw(img)
    d.text((10, 10), msg, fill=inky.BLACK, font=font)
    d.text((10, 40), f"Itens: {count}", fill=inky.BLACK, font=font)
    inky.set_image(img)
    inky.show()
