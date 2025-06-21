from inky.auto import auto
from PIL import Image, ImageDraw

inky = auto()
inky.set_border(inky.WHITE)

img = Image.new("P", (inky.WIDTH, inky.HEIGHT))
draw = ImageDraw.Draw(img)
draw.text((10, 10), "Hello Inky!", fill=inky.BLACK)

inky.set_image(img)
inky.show()
