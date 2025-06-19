from datetime import datetime
from pathlib import Path
import subprocess

PHOTO_DIR = Path("photos")
PHOTO_DIR.mkdir(exist_ok=True)

def capture_photo():
    fn = PHOTO_DIR / f"photo_{datetime.now():%Y%m%d_%H%M%S}.jpg"
    subprocess.run(["libcamera-jpeg", "-o", str(fn)], check=True)
    return fn.name

def capture_gif(frames=5, delay=0.2):
    imgs = []
    temp_files = []
    for i in range(frames):
        tf = PHOTO_DIR / f"frame_{datetime.now():%Y%m%d_%H%M%S}_{i}.jpg"
        subprocess.run(["libcamera-jpeg", "-o", str(tf)], check=True)
        temp_files.append(tf)
    gif_fn = PHOTO_DIR / f"gif_{datetime.now():%Y%m%d_%H%M%S}.gif"
    import imageio
    images = [imageio.imread(str(f)) for f in temp_files]
    imageio.mimsave(str(gif_fn), images, duration=delay)
    for f in temp_files:
        f.unlink()
    return gif_fn.name
