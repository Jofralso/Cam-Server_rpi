#!/usr/bin/env bash
set -e

# 1. Instalar dependências básicas
apt update
apt install -y libcamera-apps python3-libcamera python3-pip ffmpeg gpiozero inky python3-pillow imageio

# 2. Configuração permanente (config.txt)
echo "dtoverlay=disable-wifi" >> /boot/firmware/config.txt
echo "dtoverlay=disable-bt" >> /boot/firmware/config.txt
echo "dtparam=spi=on" >> /boot/firmware/config.txt
echo "dtparam=i2c=on" >> /boot/firmware/config.txt
echo "dtoverlay=spi0-0cs" >> /boot/firmware/config.txt  # evitar conflito CS0 com Inky
echo "arm_freq=600" >> /boot/firmware/config.txt        # subclock CPU
echo "maxcpus=1" >> /boot/firmware/cmdline.txt

# 3. Remover serviços que consumam energia
systemctl disable bluetooth.service
systemctl disable hciuart.service

# 4. Script para desligar HDMI, USB, LEDs e Wi‑Fi/Bluetooth no boot
cat <<'EOF' >> /etc/rc.local
# Otimizações de energia
/opt/vc/bin/tvservice -o                         # Desliga HDMI
echo none > /sys/class/leds/led0/trigger         # LEDs off
# USB off
echo '1-1' > /sys/bus/usb/drivers/usb/unbind
rfkill block wifi
rfkill block bluetooth
exit 0
EOF

# 5. Script Python principal
cat > /usr/local/bin/camera_daemon.py <<'EOF'
#!/usr/bin/env python3
import time, subprocess
from gpiozero import Button, RGBLED
from inky.auto import auto
from PIL import Image, ImageFont, ImageDraw
from pathlib import Path
import imageio

# Config
led = RGBLED(22,27,17)
btn = Button(5, hold_time=2)
inky = auto()
font = ImageFont.load_default()
PHOTO_DIR = Path("/home/dietpi/photos"); PHOTO_DIR.mkdir(exist_ok=True)

def show(msg, count):
    img = Image.new("P", (inky.WIDTH, inky.HEIGHT), inky.WHITE)
    d = ImageDraw.Draw(img)
    d.text((10,10), msg, inky.BLACK, font)
    d.text((10,40), f"Count: {count}", inky.BLACK, font)
    inky.set_image(img); inky.show()

count_photo = 0; count_gif = 0

def snap(): 
    global count_photo
    led.color=(1,1,0)
    fn=PHOTO_DIR/f"photo_{int(time.time())}.jpg"
    subprocess.run(["libcamera-jpeg","-o",str(fn)],check=True)
    count_photo+=1; show("Photo!",count_photo)
    led.color=(0,1,0)

def gif():
    global count_gif
    led.color=(0,0,1)
    frames=[]
    for i in range(5):
        tf=PHOTO_DIR/f"frame_{time.time()}_{i}.jpg"
        subprocess.run(["libcamera-jpeg","-o",str(tf)],check=True)
        frames.append(imageio.imread(str(tf)))
        Path=tf
    fn=PHOTO_DIR/f"gif_{int(time.time())}.gif"
    imageio.mimsave(str(fn), frames, duration=0.2)
    count_gif+=1; show("GIF!",count_gif)
    led.color=(0,1,0)

btn.when_pressed = snap
btn.when_held = gif

# loop principal
led.color=(0,1,0); show("Ready",0)
while True:
    time.sleep(1)
EOF
chmod +x /usr/local/bin/camera_daemon.py

# 6. Service systemd
cat > /etc/systemd/system/camera.service <<'EOF'
[Unit]
Description=Camera Daemon with low power
After=multi-user.target

[Service]
ExecStart=/usr/local/bin/camera_daemon.py
User=dietpi
Environment=HOME=/home/dietpi
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable camera.service

echo "Setup concluído. Reboot para ativar modo câmera."
