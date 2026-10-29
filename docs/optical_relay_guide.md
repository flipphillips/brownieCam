# Premo Junior 1A Optical Relay Design Guide

## 1. Specifications & Dimensions

* **Camera Model**: Premo Junior No. 1A (Rochester Optical Co. / Eastman Kodak Co., c. 1907–1920s)
* **Original Film Format**: Type 116 roll film
* **Original Negative Size**: 2½ × 4¼ inches (~64 mm × 108 mm)
* **Original Lens**: Front-mounted Meniscus / Achromatic Doublet (approx. $f = 110\text{ mm}$ to $125\text{ mm}$, fixed at $\approx f/11 - f/14$)
* **Focal Plane Location**: Located at the rear aperture of the removable inner wooden/metal cone.

---

## 2. Why the Relay Method Works

A normal digital sensor placed at the film gate only captures a 6×8mm slice of the center, acting as an extreme 12x telephoto lens. 

In the **Ground Glass Relay** method:
1. The original Premo lens projects its full image circle onto a frosted optical screen placed exactly where the 116 film used to travel.
2. The screen captures the true depth-of-field, edge vignetting, aberrations, and perspective of the vintage optics.
3. A modern digital camera sensor with a macro/wide lens photographs the back of that ground glass screen.

```
[Subject] ---> (Premo Lens) 
                   |
                   v (Focal length ~115mm)
           [Ground Glass Screen] (64mm x 108mm image formed here)
                   |
                   v (Relay distance: ~45mm to 80mm)
           (Macro/Wide Lens)
                   |
            [Pi HQ / V3 Sensor] ---> [Pi Zero 2 W] ---> [MicroSD / Wi-Fi]
```

---

## 3. Packaging Inside the Premo Box: The Folded Mirror Path

Because the Premo Junior 1A has a removable inner carrier and two large cavities where the wooden 116 spools used to sit (top and bottom), the most elegant way to fit the relay **completely inside without modifying the exterior leatherette** is a folded optical path:

```
+-------------------------------------------------------+
|  Top Spool Chamber:                                   |
|  [LiPo Battery 18650 / 2500mAh + Charging Board]      |
+-------------------------------------------------------+
|  Focal Plane:                                         |
|  [Ground Glass Screen]                                |
|         \                                             |
|          \  <-- 45° First-Surface Mirror              |
|           \                                           |
|            | (Light reflected downwards)              |
|            v                                          |
+-------------------------------------------------------+
|  Bottom Spool Chamber:                                |
|  [Macro / Wide Lens pointing UP at mirror]            |
|  [Pi HQ Camera or Camera V3]                          |
|  [Raspberry Pi Zero 2 W]                              |
+-------------------------------------------------------+
```

### Why use a 45° First-Surface (Front-Surface) Mirror?
* **Zero Ghosting**: Standard bathroom mirrors reflect off the back of the glass, creating a secondary faint double reflection ("ghosting"). A front-surface mirror (available cheaply on eBay/Amazon or salvaged from an old flatbed scanner) reflects directly off the coating.
* **Compact Path**: It turns the optical path 90°, turning the vertical height of the box into optical throw distance (giving ~70mm of room for the relay lens to focus cleanly across the entire screen).

---

## 4. Ground Glass Material Selection

To avoid severe hotspotting (bright glowing spot in the center with dark corners):
1. **Option A: High-Grit Etched Glass (Best fidelity)**
   * Borosilicate glass or microscope slides ground with 1500–2000 grit silicon carbide or aluminum oxide slurry.
2. **Option B: Drafting Film / Matte Mylar (Easiest)**
   * Frosted drafting film (matte polyester) stretched flat across an acrylic carrier plate. Produces very subtle, pleasant vintage diffusion.
3. **Hotspot Mitigation: Thin Fresnel Field Lens**
   * Placing a credit-card-sized flat Fresnel lens directly against the front or back of the ground glass collimates the incoming light cone from the Premo lens straight into the Pi camera lens.

---

## 5. Shutter Trigger Mechanisms

The Premo Junior 1A has an external lever that trips a spring-loaded rotary blade.

1. **Option 1: Microswitch on the Lever (Recommended)**
   * Glue a sub-miniature tactile limit switch (or Omron lever switch) inside the front bezel directly under the path of the original shutter trip arm.
   * Lock the rotary blade in the "open" position.
   * Pulling the original lever clicks the switch, giving an authentic tactile feel while the Pi controls exposure electronically.
2. **Option 2: Optical Interrupter**
   * Keep the original mechanical shutter firing (approx. 1/30s to 1/50s).
   * Place an infrared slotted optical switch across the blade path.
   * When light passes through, the Pi captures a fast rolling shutter frame. *(Note: Requires bright daylight due to the short mechanical exposure).*
