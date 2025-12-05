# image_utility.py
from __future__ import annotations
import random
from image.rgba import RGBA
from image.bitmap import Bitmap


class ImageUtility:

    # --------------------------------------------------------------
    # recolor_white (0–1 logic)
    # --------------------------------------------------------------
    @classmethod
    def recolor_white(cls, bitmap: Bitmap, rgba: RGBA, color_noise: float) -> None:
        """
        Recolor every pixel based on the RGBA baseline color,
        with noise entirely in 0–1 space.

        baseline.r  ±  (color_noise / 2)
        """
        half = color_noise / 2.0

        base_r = rgba.rf   # 0–1
        base_g = rgba.gf
        base_b = rgba.bf

        w, h = bitmap.width, bitmap.height

        for x in range(w):
            for y in range(h):
                px = bitmap.rgba[x][y]

                # noise in 0-1 space
                modified_r = base_r + random.uniform(-half, +half)
                modified_g = base_g + random.uniform(-half, +half)
                modified_b = base_b + random.uniform(-half, +half)

                # clamp to 0–1
                modified_r = max(0.0, min(1.0, modified_r))
                modified_g = max(0.0, min(1.0, modified_g))
                modified_b = max(0.0, min(1.0, modified_b))

                # convert back to 0–255 for RGBA constructor
                bitmap.rgba[x][y] = RGBA(
                    int(modified_r * 255),
                    int(modified_g * 255),
                    int(modified_b * 255),
                    px.ai,   # alpha unchanged, still 0–255
                )

    # --------------------------------------------------------------
    # multiply_alpha (0–1 logic)
    # --------------------------------------------------------------
    @classmethod
    def multiply_alpha(cls, bitmap: Bitmap, base: float, alpha_noise: float) -> None:
        """
        Multiply alpha by a noisy factor, with all math in 0–1 space:

            factor = base ± (alpha_noise / 2)

        If original alpha is 0, it remains 0.
        """
        half = alpha_noise / 2.0

        w, h = bitmap.width, bitmap.height

        for x in range(w):
            for y in range(h):
                px = bitmap.rgba[x][y]

                # original alpha in 0–1
                orig_alpha_f = px.af

                if orig_alpha_f == 0.0:
                    continue

                # noisy factor
                factor = base + random.uniform(-half, +half)
                factor = max(0.0, min(1.0, factor))

                new_alpha_f = orig_alpha_f * factor
                new_alpha_i = int(new_alpha_f * 255)

                bitmap.rgba[x][y] = RGBA(
                    px.ri,
                    px.gi,
                    px.bi,
                    new_alpha_i,
                )
