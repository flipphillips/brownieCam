# 📷 BrownieCam: Digital Premo Junior 1A Retrofit

Convert an antique **Rochester Optical / Eastman Kodak Premo Junior No. 1A** (or Brownie-style box camera) into a modern digital camera while preserving the authentic full-frame character, depth of field, and vignetting of the original vintage optics.

---

## 🔍 How It Works: The Ground-Glass Relay

Instead of mounting a tiny modern digital sensor directly at the film gate (which creates an extreme 12× telephoto crop that cuts out all vintage lens character), BrownieCam uses an **optical ground-glass relay**:

1. The Premo's front meniscus lens forms a full-sized 64 × 108 mm image onto a fine frosted optical screen (ground glass or drafting film) sitting at the original 116 film plane.
2. A 45° front-surface mirror reflects that image downward into the empty lower spool chamber.
3. A Raspberry Pi Camera (with a wide/macro lens) captures the image off the screen.
4. Pressing the original external shutter lever triggers the Pi via GPIO, processing the image and saving it to disk.
5. An onboard Wi-Fi web gallery lets you review and download photos from your phone in the field!

```
                       +---------------------------------------+
                       |           Premo Junior 1A             |
                       |                                       |
Original Lens/Bezel -->| [Front Meniscus Lens]                 |
                       |          |                            |
Original Shutter ----->| [Lever] -> [Microswitch / Reed Switch]|
                       |                    |                  |
                       |                    v (GPIO 17)        |
Focal Plane ---------->| [Ground Glass Screen]                 |
                       |         \                             |
                       |          \ (45° First-Surface Mirror) |
                       |           v                           |
Spool Chamber -------->| [Pi Camera + Macro Lens]              |
                       |          | (CSI Ribbon)               |
                       |          v                            |
Electronics ---------->| [Raspberry Pi Zero 2 W]               |
                       | [LiPo 18650 Battery + 5V Boost]       |
                       +---------------------------------------+
```

---

## 🛠️ Repository Contents

* [`src/config.py`](file:///Users/fxpppr/GitHub/brownieCam/src/config.py): Configuration for GPIO pins, optical flips, resolutions, and film aspect ratios.
* [`src/camera_daemon.py`](file:///Users/fxpppr/GitHub/brownieCam/src/camera_daemon.py): Main capture service with hardware debouncing, Picamera2 integration, auto-flips, and mock testing support.
* [`src/web_viewer.py`](file:///Users/fxpppr/GitHub/brownieCam/src/web_viewer.py): Mobile-optimized photo gallery accessible via local Wi-Fi.
* [`docs/optical_relay_guide.md`](file:///Users/fxpppr/GitHub/brownieCam/docs/optical_relay_guide.md): Optical calculations, ground glass materials, and folded-mirror packaging.
* [`docs/wiring_and_hardware.md`](file:///Users/fxpppr/GitHub/brownieCam/docs/wiring_and_hardware.md): GPIO pinout table, battery power delivery, and switch options.

---

## 🚀 Quickstart & Testing

### 1. Test on your Computer (Mock Mode)
You can run the daemon and web gallery right now on macOS/Linux without hardware connected:

```bash
# Install dependencies
pip install -r requirements.txt

# Take a simulated test shot
python3 src/camera_daemon.py --test-shot

# Launch the mobile web gallery
python3 src/web_viewer.py
```
Open [http://localhost:8080](http://localhost:8080) in your browser to view the gallery.

### 2. Deploying to Raspberry Pi
On Raspberry Pi OS (Bookworm or Bullseye):

```bash
# 1. Install native camera libraries
sudo apt update
sudo apt install -y python3-picamera2 python3-libcamera python3-gpiozero python3-pil python3-flask

# 2. Clone repo and start daemon
python3 src/camera_daemon.py
```

To run automatically at boot, create a systemd service:
```bash
sudo cp systemd/brownie.service /etc/systemd/system/
sudo systemctl enable --now brownie.service
```

---

## 🔌 Hardware Connections Summary

| Pin | BCM GPIO | Connects To | Purpose |
| :--- | :--- | :--- | :--- |
| **Pin 11** | GPIO 17 | Shutter Microswitch (to GND) | Shutter Trigger (Internal pull-up) |
| **Pin 13** | GPIO 27 | Status LED Anode (via 220Ω to GND) | Solid = Ready, Pulse = Saving |
| **Pin 15** | GPIO 22 | Pushbutton (to GND) | Hold 3s for safe shutdown |
| **Pin 2** | 5V | Battery Boost +5V Out | System Power |
| **Pin 6** | GND | Battery Boost GND | Common Ground |

See [`docs/wiring_and_hardware.md`](file:///Users/fxpppr/GitHub/brownieCam/docs/wiring_and_hardware.md) for full schematics and details.
