# genxyz — Synthetic Pixel-Level Circle Dataset

This repository contains a fully synthetic pixel-level annotation dataset intended for
**pipeline calibration**, **infrastructure testing**, and **algorithm bring-up**.  
It is **not** a challenging vision dataset. Instead, it provides extremely simple,
high-signal circular objects rendered over randomized microscope-style backgrounds.

The goal is to give developers a controlled environment to verify:

- That their data-loading pipeline works end-to-end  
- That pixel-accurate masks are read and interpreted correctly  
- That augmentation, batching, and coordinate transforms behave as expected  
- That segmentation or detection models can overfit on something trivial  

This dataset is deliberately easy. It helps you confirm your system is wired together correctly **before** throwing real, messy biological data at it.

---

## What the Dataset Contains

Each generated sample includes two files:

1. **`<name>.png`**  
   A 256×256 RGB image containing 0–N translucent circles with randomized:
   - position  
   - radius  
   - color (chosen from a fixed palette)  
   - alpha blending  
   - per-pixel color noise  
   - per-pixel alpha noise  

   The background is selected from a library of dish-style microscope photographs,
   randomly rotated, flipped, resized, and cropped.

2. **`<name>_annotations.json`**  
   A JSON document storing the exact pixel mask locations of the circles drawn.

   Each circle is represented by a `DataLabel` object:

```
{
"name": "Red",
"pixels": [
{ "y": 101, "x_start": 87, "x_end": 92 },
{ "y": 102, "x_start": 85, "x_end": 94 },
...
]
}
```

Pixel runs use a horizontal run-length format for compactness.  
All pixel coordinates are **absolute image-space coordinates**, after placement,
recoloring, alpha scaling, and stamping.

---

## Intended Uses

This dataset is designed for:

### • Testing segmentation pipelines  
If your mask loader, decoder, model, loss functions, and training loop are wired
correctly, a UNet-type model should achieve **~100% pixel accuracy almost immediately**.

### • Probing coordinate-transform errors  
Since all objects are circles, any skew or stretching in your masks can be spotted easily.

### • Debugging batching and augmentation  
Rotations, flips, crops, and color jitter should preserve circularity.

### • Ensuring label ↔ image alignment  
Every mistake in mask alignment produces very obvious visual errors.

---

## Not Intended For

This dataset is *not* useful for:

- Learning real cell morphology  
- Training production models  
- Studying edge cases in medical imaging  
- Evaluating complex segmentation architectures  

These targets are simple, perfect circles — they exist purely to confirm that
your system can learn something trivial before you move on to real data.

---