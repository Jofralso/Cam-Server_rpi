# Raspberry Pi Zero 2W Camera Server with Inky pHAT

![Project Banner](./static/banner.png)

---

## Overview

This project transforms a **Raspberry Pi Zero 2W** equipped with an **OV5640 camera** and an **Inky pHAT e-paper display** into a smart, standalone camera system. It captures photos and animated GIFs, displays witty status updates and photo counts on the Inky pHAT with an Apple-inspired mascot, and serves a web interface for browsing and downloading saved media.

Ideal for battery-powered deployments or situations where a lightweight, low-power photo server is required.

---

## Features

- **Capture photos and animated GIFs** using the OV5640 camera module  
- **Inky pHAT display** shows status messages, photo count, power state, and fun Apple-inspired mascot animations  
- **Single multifunction button** controls capture modes and power, with feedback from an RGB LED (Red/Green/Blue)  
- **Lightweight Flask web server** streams saved photos and GIFs accessible from any browser on your network  
- **Battery-saving standalone mode** with camera-only operation (no WiFi needed)  
- **Docker-ready** for easy deployment and consistency across environments  
- **Comprehensive automated testing** with `pytest` and `tox` ensures reliability  

---

## Hardware Setup

### Components

- **Raspberry Pi Zero 2W**  
- **OV5640 camera module** (connected to CSI interface)  
- **Inky pHAT** e-paper display (SPI interface)  
- **Multifunction button** wired to GPIO17 (configurable)  
- **RGB LED** wired to GPIO18 (Red), GPIO23 (Green), GPIO24 (Blue)  

### Wiring Notes

- SPI pins are shared between the camera and Inky pHAT; only one SPI device should be active at a time.  
- Connect the button and RGB LED to the indicated GPIOs on the Pi’s lower header (soldar na parte inferior).  
- Use appropriate resistors for LEDs and button pull-up/down configuration.  

---

## Software Setup

### Requirements

- Raspberry Pi OS Lite or DietPi (tested on both)  
- Python 3.11 with virtual environment support  
- Docker and Docker Compose (optional, for container deployment)  

### Installation

Clone the repository on your Raspberry Pi or development machine:

```bash
git clone https://github.com/yourusername/cam-server.git
cd cam-server
````

Create and activate a Python virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Alternatively, build and run the Docker container:

```bash
docker-compose up --build
```

### Camera Mode Setup (Standalone)

Run the camera mode setup script to enable the camera and disable SPI (for power saving):

```bash
sudo ./setup_camera_mode.sh
```

Reboot your Pi to apply changes:

```bash
sudo reboot
```

---

## Usage

Start the main application:

```bash
python app.py
```

Or with Docker (already running from above):

```bash
docker-compose up
```

Open a browser on your local network and navigate to:

```
http://<pi_ip_address>:5000
```

You will see the live gallery of photos and GIFs saved on the device.

---

## Button & LED Controls

| Action                | Button Press                | LED Color       | Inky pHAT Message             |
| --------------------- | --------------------------- | --------------- | ----------------------------- |
| Power On              | Long press                  | Green           | "Power On" + mascot animation |
| Capture Photo         | Single press                | Blue (blinking) | "Photo Saved! Count: N"       |
| Capture GIF Animation | Double press                | Purple          | "GIF Saved! Count: N"         |
| Power Off             | Long press (hold 5 seconds) | Red             | "Powering Down..."            |

---

## Testing

We use `pytest` and `tox` for automated testing, including mocks for hardware interfaces so you can test anywhere.

To run tests and lint checks:

```bash
tox
```

This runs:

* Unit tests for camera capture, Flask API, button & LED logic, Inky pHAT display
* Code style checks and auto-fixes with `ruff`
* Coverage reports for test completeness

---

## Screenshots

![Web Gallery](./static/screenshots/web_gallery.png)
*Photo gallery served by the Flask app.*

![Inky pHAT Status](./static/screenshots/inky_status.png)
*Inky pHAT display showing mascot and photo count.*

---

## Contribution & Support

Feel free to contribute! Open issues and pull requests are welcome.
For questions, please open an issue or contact the maintainer.

---

## License

This project is licensed under the **MIT License**. See [LICENSE](./LICENSE) for details.

---

Thank you for checking out the Raspberry Pi Camera Server project!
Bring your Pi to life as a smart, battery-efficient camera with personality.

---

*Made with ❤️ for makers, hackers, and creative coders.*

