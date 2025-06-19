# Raspberry Pi Zero 2W Camera Server with Inky pHAT

## Overview

This project turns a Raspberry Pi Zero 2W with an OV5640 camera and an Inky pHAT display into a standalone camera system.  
It captures photos and animated GIFs, displays status messages on the Inky pHAT, and serves saved images via a simple web server.

---

## Features

- Capture photos and animated GIFs from OV5640 camera  
- Inky pHAT displays status messages like power on/off, photo count, saving, server status, etc., with a fun Apple-inspired mascot  
- External button and RGB LED control all main functions (capture photo, capture gif, power on/off)  
- Built-in Flask server to view and download saved photos and gifs over the network  
- Battery saving mode: can operate standalone without WiFi, acting purely as a camera

---

## Hardware Connections

- **Camera:** OV5640 connected via CSI  
- **Inky pHAT:** Connected via SPI (pins need to be shared carefully with camera; no simultaneous SPI use)  
- **Button:** Connected to GPIO17 (example, configurable)  
- **RGB LED:** Connected to GPIO18 (Red), GPIO23 (Green), GPIO24 (Blue)  
- **Power:** Use appropriate power supply for Raspberry Pi Zero 2W

---

## Software Setup

- Runs on DietPi or Raspberry Pi OS Lite  
- Python 3.11 environment with dependencies managed via `requirements.txt` and virtualenv  
- Main scripts in `scripts/` folder: camera capture, button & LED manager, Inky pHAT display controller  
- Flask web app in `app.py` serves images and status API  
- Uses `libcamera` for camera control  

---

## Running the Project

1. Clone the repo and set up Python environment  
2. Run `main.py` to start camera service and web server  
3. Access the web interface via `http://<pi_ip>:5000` to view photos  
4. Use the button to capture photos or gifs; LED and Inky pHAT indicate status  

---

## Testing

This project includes a comprehensive automated test suite using **pytest** and **tox**:

- Unit tests for camera capture, Flask endpoints, button/LED logic, and Inky display  
- Hardware interactions are mocked for safe testing on any system  
- Linting with **ruff** is integrated into `tox`  
- Run tests and lint with:

```bash
tox
````

* Tests ensure code reliability and help maintain battery-saving standalone functionality

---

## Notes

* When running as a standalone camera (without WiFi), the server is still active on localhost for local interactions or USB networking
* SPI pins are shared between Inky pHAT and camera — only one SPI device active at a time
* Button controls multiple modes; LED colors reflect current state (e.g., red for error, green for ready)
* The Inky pHAT displays fun status messages and counts with an Apple-inspired mascot for engagement

---

## License

MIT License — see LICENSE file

---

## Contributions

Contributions welcome! Please open issues or pull requests for bug fixes, features, or documentation improvements.

---

## Contact

For questions or support, open an issue on GitHub or contact the maintainer.

