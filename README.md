# 📸 Cam‑Server with Inky pHAT (Standalone Pi Zero 2 W)

Turn your Raspberry Pi Zero 2 W (DietPi) into a **fully standalone camera** with:

- CSI camera (OV5640) capturing photos and GIFs  
- **Physical button**:
  - Short press → take photo  
  - Long press → take GIF  
- **RGB LED** shows status:
  - Green → ready  
  - Yellow → photo  
  - Blue → GIF  
  - Red → off  
- **Inky pHAT** displays messages and count  
- **Flask web server** hosts a local gallery (no Internet required)

---

## 🔋 Low Power / Offline Mode

The system is optimized to **maximize battery life**:

- Disables HDMI, Wi‑Fi, Bluetooth, USB, and onboard LEDs  
- Underclocks the CPU (600 MHz, single core)  
- Runs **offline**, no Internet needed

Energy-saving steps referenced from the official Raspberry Pi power guide :contentReference[oaicite:1]{index=1}, including disabling HDMI, USB, Wi‑Fi, Bluetooth, LEDs, and setting a lower CPU frequency.

---

## 🌐 Local Server Access (No Internet Required)

Yes — you can run the server without any Internet connection. You just need **local network access** to connect via browser:

### 1. Using an existing network (router)
Connect the Pi to your Wi‑Fi (through the router). Even without Internet, devices on the same network can visit:
```

http\://\<PI\_IP>:8000

```

### 2. Direct hotspot mode
Configure the Pi as a **Wi‑Fi Access Point (AP)** with DHCP (no NAT/Internet). Devices like your phone or laptop can directly connect to the Pi:
```

[http://192.168.4.1:8000](http://192.168.4.1:8000)

````
Ideal for field use — fully autonomous operation 

---

## ⚙️ Installation & Setup

Clone the repository, then choose your setup:

### A. Using Docker
```bash
docker-compose up --build -d
````

### B. Without Docker (using Python virtual environment)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

---

## 🧠 How It Works

* **Button actions**:

  * Short press → photo
  * Long press (2s) → GIF (5 frames)
* **LED RGB** indicates:

  * Green – system ready
  * Yellow – photo capture
  * Blue – GIF capture
  * Red – system off
* **Inky pHAT** shows messages & counts
* **Server endpoints**:

  * `/` → gallery display
  * `/photos/<filename>` → serve file
  * `/api/status` → JSON with photo + GIF counters

Button-triggered actions are safe even when offline; flash storage is local.

---

## 🧭 Next Steps & Enhancements

* Add **live video streaming** using MJPEG/libcamera
* Implement **backup and sync** (Google Drive, Dropbox)
* Enable Pi **hotspot configuration on first boot**, if no router detected
* Add **double press** to reboot or **hold hold** to shut down

---

## 📝 Offline Access Summary

| Mode                    | Local Access? | Internet Required? |
| ----------------------- | ------------- | ------------------ |
| Connected to router     | ✅             | ❌                  |
| Access Point standalone | ✅             | ❌                  |

No external infrastructure is required—just power the Pi, and it's a functioning camera + server!

---

## 📋 References

* Disable hardware (HDMI, Wi‑Fi, Bluetooth, LEDs, USB) for power saving ([blues.com][1], [peppe8o.com][2], [dietpi.com][3], [raspberrypi.stackexchange.com][4], [forums.raspberrypi.com][5])
* Raspberry Pi as an offline Access Point (AP mode) ([forums.raspberrypi.com][5])
* Build Access Point without Internet (via DietPi tools) ([dietpi.com][6])

---

## 🏁 Conclusion

You're building a **battery-powered, standalone photo/GIF camera**, fully headless, with live gallery access—all without needing the Internet. Just power it, press the button, and share the content via Wi‑Fi.

Ready to roll!
