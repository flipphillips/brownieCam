"""
Configuration settings for BrownieCam (Premo Junior 1A Digital Retrofit)
"""

import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
PHOTO_DIR = Path(os.environ.get("BROWNIE_PHOTO_DIR", BASE_DIR / "photos"))
PHOTO_DIR.mkdir(parents=True, exist_ok=True)

# Hardware GPIO Pins (BCM numbering)
PIN_SHUTTER = int(os.environ.get("PIN_SHUTTER", 17))       # Pin 11 on header (active LOW with internal pull-up)
PIN_STATUS_LED = int(os.environ.get("PIN_STATUS_LED", 27))  # Pin 13 on header (indicates ready / saving)
PIN_SHUTDOWN = int(os.environ.get("PIN_SHUTDOWN", 22))      # Pin 15 on header (hold for 3s to cleanly shut down Pi)

# Optical & Inversion Settings
# The image on a ground glass screen is naturally inverted (upside-down & reversed).
# If a 45-degree folding mirror is used, one axis will be inverted.
# Adjust these flips to match your mechanical assembly:
IMAGE_HFLIP = os.environ.get("IMAGE_HFLIP", "true").lower() == "true"
IMAGE_VFLIP = os.environ.get("IMAGE_VFLIP", "true").lower() == "true"
IMAGE_ROTATION = int(os.environ.get("IMAGE_ROTATION", 0))  # 0, 90, 180, or 270

# Aspect Ratio / Framing
# Original 116 film format had a 2.5 x 4.25 inch frame (~1:1.7 aspect ratio).
# Set CROP_TO_VINTAGE_GATE to True to automatically crop the relay capture
# to the vintage film window boundaries.
CROP_TO_VINTAGE_GATE = os.environ.get("CROP_TO_VINTAGE_GATE", "false").lower() == "true"
VINTAGE_ASPECT_RATIO = 4.25 / 2.5  # ~1.7:1 (or 1:1.7 depending on orientation)

# Camera Capture Parameters
CAPTURE_RESOLUTION = (4056, 3040)  # Full resolution for Pi HQ Camera (IMX477)
# For Pi Camera Module 3 (IMX708), use (4608, 2592)
SAVE_RAW = os.environ.get("SAVE_RAW", "false").lower() == "true"

# Web Server Settings
WEB_HOST = os.environ.get("WEB_HOST", "0.0.0.0")
WEB_PORT = int(os.environ.get("WEB_PORT", 8080))
