#!/usr/bin/env python3
"""
BrownieCam Shutter & Capture Daemon

Monitors the mechanical shutter switch via GPIO, triggers high-resolution capture
through the relay lens onto the ground glass screen, corrects orientation/flips,
and saves the image to disk with metadata.
"""

import sys
import time
import signal
import logging
from datetime import datetime
from pathlib import Path
from PIL import Image

import config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("brownieCam")

# Hardware detection and graceful fallback
try:
    from gpiozero import Button, LED
    GPIO_AVAILABLE = True
except (ImportError, Exception) as e:
    logger.warning(f"gpiozero not available: {e}. Running in simulation mode for GPIO.")
    GPIO_AVAILABLE = False

try:
    from picam2 import Picamera2
    PICAMERA_AVAILABLE = True
except ImportError:
    logger.warning("Picamera2 not installed. Running in mock camera mode.")
    PICAMERA_AVAILABLE = False


class BrownieCamera:
    def __init__(self):
        self.camera = None
        self.led = None
        self.shutter_btn = None
        self.shutdown_btn = None
        self.running = True

        self._setup_camera()
        self._setup_gpio()

    def _setup_camera(self):
        if PICAMERA_AVAILABLE:
            try:
                self.camera = Picamera2()
                camera_config = self.camera.create_still_configuration(
                    main={"size": config.CAPTURE_RESOLUTION}
                )
                self.camera.configure(camera_config)
                self.camera.start()
                # Allow sensor auto-exposure and white balance to settle
                time.sleep(1.5)
                logger.info("Picamera2 initialized and streaming preview.")
            except Exception as e:
                logger.error(f"Failed to initialize Picamera2: {e}")
                self.camera = None
        else:
            logger.info("Mock camera active (generates synthetic ground-glass frames).")

    def _setup_gpio(self):
        if GPIO_AVAILABLE:
            try:
                self.led = LED(config.PIN_STATUS_LED)
                self.led.on()  # Solid on indicates ready

                self.shutter_btn = Button(
                    config.PIN_SHUTTER,
                    pull_up=True,
                    bounce_time=0.1
                )
                self.shutter_btn.when_pressed = self.trigger_shot

                self.shutdown_btn = Button(
                    config.PIN_SHUTDOWN,
                    pull_up=True,
                    hold_time=3.0
                )
                self.shutdown_btn.when_held = self._handle_safe_shutdown

                logger.info(
                    f"GPIO initialized: Shutter=GPIO{config.PIN_SHUTTER}, "
                    f"LED=GPIO{config.PIN_STATUS_LED}, Shutdown=GPIO{config.PIN_SHUTDOWN}"
                )
            except Exception as e:
                logger.warning(f"Error initializing GPIO hardware: {e}")
        else:
            logger.info("Simulated GPIO: Press Enter in terminal or invoke trigger_shot().")

    def _handle_safe_shutdown(self):
        logger.info("Shutdown button held! Initiating safe poweroff...")
        if self.led:
            self.led.blink(on_time=0.1, off_time=0.1, n=10)
        import os
        os.system("sudo poweroff")

    def capture_frame(self) -> Image.Image:
        """Capture raw frame from camera or generate a mock test image."""
        if self.camera:
            # Capture as PIL Image directly from Picamera2
            return self.camera.capture_image()
        else:
            # Mock image for testing outside Raspberry Pi
            img = Image.new("RGB", (1200, 800), color=(240, 230, 210))
            from PIL import ImageDraw
            draw = ImageDraw.Draw(img)
            draw.text((100, 400), "BrownieCam Mock Relay Capture", fill=(40, 30, 20))
            return img

    def process_and_save(self, img: Image.Image) -> Path:
        """Applies necessary orientation flips, rotation, and vintage cropping."""
        # Ground-glass optical flip corrections
        if config.IMAGE_HFLIP:
            img = img.transpose(Image.FLIP_LEFT_RIGHT)
        if config.IMAGE_VFLIP:
            img = img.transpose(Image.FLIP_TOP_BOTTOM)
        if config.IMAGE_ROTATION != 0:
            img = img.rotate(config.IMAGE_ROTATION, expand=True)

        # Optional crop to match the 116 film aspect ratio (approx 1:1.7)
        if config.CROP_TO_VINTAGE_GATE:
            w, h = img.size
            target_aspect = config.VINTAGE_ASPECT_RATIO
            current_aspect = w / h
            if current_aspect > target_aspect:
                # Too wide: crop horizontal edges
                new_w = int(h * target_aspect)
                left = (w - new_w) // 2
                img = img.crop((left, 0, left + new_w, h))
            else:
                # Too tall: crop vertical edges
                new_h = int(w / target_aspect)
                top = (h - new_h) // 2
                img = img.crop((0, top, w, top + new_h))

        # Save with ISO-style timestamp
        filename = datetime.now().strftime("BROWNIE_%Y%m%d_%H%M%S.jpg")
        filepath = config.PHOTO_DIR / filename
        img.save(filepath, quality=95)
        logger.info(f"Photo saved successfully: {filepath}")
        return filepath

    def trigger_shot(self):
        """Action invoked when mechanical shutter lever is pulled."""
        logger.info("CLICK! Shutter triggered.")
        if self.led:
            self.led.off()  # Turn off during capture/processing

        try:
            raw_img = self.capture_frame()
            saved_path = self.process_and_save(raw_img)
        except Exception as e:
            logger.error(f"Error during capture: {e}")
        finally:
            if self.led:
                # Fast double blink then solid on
                self.led.blink(on_time=0.08, off_time=0.08, n=2)
                time.sleep(0.35)
                self.led.on()

    def run(self):
        """Main service loop."""
        logger.info("BrownieCam Daemon is running. Waiting for shutter triggers...")
        def shutdown_handler(signum, frame):
            logger.info("Stopping BrownieCam Daemon...")
            self.running = False

        signal.signal(signal.SIGINT, shutdown_handler)
        signal.signal(signal.SIGTERM, shutdown_handler)

        while self.running:
            time.sleep(0.5)

        self.cleanup()

    def cleanup(self):
        if self.camera:
            try:
                self.camera.stop()
            except Exception:
                pass
        if self.led:
            self.led.off()
        logger.info("BrownieCam cleanup complete.")


if __name__ == "__main__":
    app = BrownieCamera()
    if "--test-shot" in sys.argv:
        logger.info("Executing immediate test shot...")
        app.trigger_shot()
    else:
        app.run()
