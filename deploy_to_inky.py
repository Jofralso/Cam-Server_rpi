from inky.auto import auto
from PIL import Image

inky = inkyPHAT("black")
inky.set_border(inky.WHITE)

img = Image.open("output/inky_tirar_foto.png").convert("P")
inky.set_image(img)
inky.show()


