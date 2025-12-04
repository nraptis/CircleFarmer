# generate_circle_data.py

import math
import random
from typing import Tuple

import numpy as np
from PIL import Image, ImageDraw


def generate_circle_sample(
    width: int = 256,
    height: int = 256,
    min_circles: int = 2,
    max_circles: int = 6,
    min_radius: int = 10,
    max_radius: int = 40,
) -> Tuple[Image.Image, np.ndarray, np.ndarray]:
    """
    Returns:
        image:  PIL.Image (RGBA)
        red_mask:   (H, W) uint8 (0 or 1)
        green_mask: (H, W) uint8 (0 or 1)
    """
    # RGBA background
    img = Image.new("RGBA", (width, height), (0, 0, 0, 255))

    red_mask = np.zeros((height, width), dtype=np.uint8)
    green_mask = np.zeros((height, width), dtype=np.uint8)

    # How many circles this sample?
    n_circles = random.randint(min_circles, max_circles)

    for _ in range(n_circles):
        # Random class: 0 = red, 1 = green
        circle_class = random.choice(["red", "green"])

        radius = random.randint(min_radius, max_radius)
        cx = random.randint(radius, width - radius - 1)
        cy = random.randint(radius, height - radius - 1)

        # Draw circle on a transparent overlay
        overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay, "RGBA")

        if circle_class == "red":
            color = (255, 60, 60, 128)   # 50% alpha-ish
        else:
            color = (60, 255, 60, 128)

        bbox = (cx - radius, cy - radius, cx + radius, cy + radius)
        draw.ellipse(bbox, fill=color)

        # Alpha-composite into main image
        img = Image.alpha_composite(img, overlay)

        # Update masks (geometric, not from rendered pixels)
        yy, xx = np.ogrid[:height, :width]
        dist_sq = (xx - cx) ** 2 + (yy - cy) ** 2
        inside = dist_sq <= radius ** 2

        if circle_class == "red":
            red_mask[inside] = 1
        else:
            green_mask[inside] = 1

    return img, red_mask, green_mask



if __name__ == "__main__":
    img, red_mask, green_mask = generate_circle_sample()

    # For debugging: save images
    img.save("sample_circles.png")

    Image.fromarray((red_mask * 255).astype(np.uint8)).save("sample_red_mask.png")
    Image.fromarray((green_mask * 255).astype(np.uint8)).save("sample_green_mask.png")

