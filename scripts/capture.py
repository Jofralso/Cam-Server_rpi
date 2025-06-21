import subprocess
import time
from pathlib import Path
import yaml

cfg = yaml.safe_load(open('config.yaml'))
photo_dir = Path(cfg['paths']['photos'])
photo_dir.mkdir(exist_ok=True)

def capture_photo():
    timestamp = int(time.time())
    photo_path = photo_dir / f'photo_{timestamp}.jpg'
    cmd = [
        "libcamera-still",
        "--timeout", "1000",       # 1 segundo para preview e ajuste
        "--width", str(cfg['camera']['resolution'][0]),
        "--height", str(cfg['camera']['resolution'][1]),
        "-o", str(photo_path)
    ]
    subprocess.run(cmd, check=True)
    return photo_path

def capture_gif():
    timestamp = int(time.time())
    gif_path = photo_dir / f'gif_{timestamp}.gif'
    # Captura 5 segundos a 5 fps para gif rápido e baixa qualidade
    cmd = [
        "libcamera-vid",
        "--timeout", "5000",        # 5 segundos de gravação
        "--framerate", "5",
        "--width", "320",           # baixa resolução para gif
        "--height", "240",
        "-o", "/tmp/video.h264"
    ]
    subprocess.run(cmd, check=True)
    # Converter para gif usando ffmpeg + imagemagick
    cmd_ffmpeg = [
        "ffmpeg",
        "-y",
        "-i", "/tmp/video.h264",
        "-vf", "fps=5,scale=320:-1:flags=lanczos",
        "/tmp/out.gif"
    ]
    subprocess.run(cmd_ffmpeg, check=True)

    # Mover gif para pasta fotos
    subprocess.run(["mv", "/tmp/out.gif", str(gif_path)], check=True)
    return gif_path
