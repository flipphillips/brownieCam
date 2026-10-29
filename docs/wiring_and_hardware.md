# BrownieCam Wiring & Hardware Guide

## 1. Raspberry Pi GPIO Pinout

We use the standard 40-pin header on Raspberry Pi Zero / Zero 2 W:

```
        3.3V (Pin 1)  [x] [ ]  5V (Pin 2)  <-- +5V from PowerBoost / BMS
      GPIO 2 (Pin 3)  [ ] [ ]  5V (Pin 4)
      GPIO 3 (Pin 5)  [ ] [x]  GND (Pin 6) <-- Common Ground
      GPIO 4 (Pin 7)  [ ] [ ]  GPIO 14 (Pin 8)
                 GND  [ ] [ ]  GPIO 15 (Pin 10)
   GPIO 17 (Pin 11)   [x] [ ]  GPIO 18 (Pin 12)
   GPIO 27 (Pin 13)   [x] [ ]  GND (Pin 14)
   GPIO 22 (Pin 15)   [x] [ ]  GPIO 23 (Pin 16)
        ...           [ ] [ ]  ...
                 GND  [x] [ ]  (Pin 39)
```

| Component | Pi Physical Pin | BCM GPIO | Notes |
| :--- | :--- | :--- | :--- |
| **Shutter Switch** | Pin 11 | GPIO 17 | Connect between GPIO 17 and GND. Internal pull-up is enabled. |
| **Status LED (+) / Anode** | Pin 13 | GPIO 27 | Connect via 220Ω resistor to Pin 13. |
| **Status LED (-) / Cathode**| Pin 14 | GND | Connect to ground. |
| **Safe Shutdown Button** | Pin 15 | GPIO 22 | Connect between GPIO 22 and GND. Hold 3s to safely halt Linux. |
| **5V Power Input** | Pin 2 or 4 | 5V | From 5V output of battery boost board. |
| **Ground** | Pin 6 | GND | Common system ground. |

---

## 2. Power Supply & Battery System

### Recommended Power Setup:
* **Cell**: 18650 Li-ion battery (3.7V nominal, ~2500–3500mAh) or a flat 3.7V LiPo pouch cell.
* **Charger/Boost Board**: 
  * Adafruit PowerBoost 1000 Basic or 1000C (has load-sharing and USB-C/Micro-USB charging).
  * Alternatively: A TP4056 charge board paired with an MT3608 or 5V boost regulator.

```
 [18650 Li-ion Cell]
        |
        v
 [TP4056 / PowerBoost] ---> [USB-C Port for Charging]
        | (Boost to 5V)
        v
  [Power Switch] ---------> [Pi Zero 2 Pin 2 (5V)] & [Pin 6 (GND)]
```

### Current Consumption:
* **Pi Zero 2 W idle**: ~120–180mA @ 5V
* **Pi Zero 2 W during capture & save**: ~350–500mA @ 5V
* A 2500mAh battery delivers **6 to 10+ hours** of shooting on a single charge!

---

## 3. Shutter Trigger Switch Options

* **Tactile Microswitch**: Can be hot-glued or bracketed inside the front box behind the shutter lever. When the lever reaches the bottom of its stroke, it depresses the switch.
* **Miniature Reed Switch**: Mount a small glass reed switch inside the front panel and affix a 3mm × 1mm neodymium magnet to the moving metal shutter blade. Provides 100% non-contact, friction-free triggering.
