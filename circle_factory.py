# circle_factory.py
from __future__ import annotations
import random
from bitmap import Bitmap


class CircleFactory:
    """
    Provides random circle glyph Bitmaps from the local resources folder.

    Chooses randomly from:
        circle_white_36.png
        circle_white_40.png
        circle_white_46.png
        circle_white_64.png
        circle_white_70.png
        circle_white_80.png

    All images are expected to exist under:
        /Users/naraptis/Desktop/CircleFarmer/images/circles/
    as local project resources.

    Usage:
        bmp = CircleFactory.random()
    """

    # List of all sprite filenames (no extension needed)
    _NAMES = [
        "circle_white_36",
        "circle_white_40",
        "circle_white_46",
        "circle_white_64",
        "circle_white_70",
        "circle_white_80",
    ]

    # Subdirectory as your Bitmap loader expects
    _SUBDIR = "/images/circles/"
    _EXT = ".png"

    @classmethod
    def random(cls) -> Bitmap:
        """
        Return a randomly selected circle sprite as a Bitmap.
        """
        name = random.choice(cls._NAMES)
        full_name = name + cls._EXT

        return Bitmap.with_local_image(
            subdirectory=cls._SUBDIR,
            name="/" + full_name   # match your example usage
        )
