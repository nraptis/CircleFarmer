# circle_factory.py
from __future__ import annotations
import random
from image.bitmap import Bitmap


class CircleFactory:
    """
    Provides random circle glyph Bitmaps from the local resources folder.

    Chooses randomly from:
        circle_white_36.png
        circle_white_38.png
        circle_white_40.png
        circle_white_42.png
        circle_white_44.png
        circle_white_46.png
        circle_white_48.png
        circle_white_50.png
        circle_white_52.png
        circle_white_54.png
        circle_white_56.png
        circle_white_58.png
        circle_white_60.png
        circle_white_62.png
        circle_white_64.png
        circle_white_66.png
        circle_white_68.png
        circle_white_70.png
        circle_white_72.png
        circle_white_74.png
        circle_white_76.png
        circle_white_78.png
        circle_white_80.png
        circle_white_82.png
        circle_white_84.png
        circle_white_86.png
        circle_white_88.png
        circle_white_90.png
        circle_white_92.png
        circle_white_94.png

    All images are expected to exist under:
        /Users/naraptis/Desktop/CircleFarmer/images/circles/
    as local project resources.

    Usage:
        bmp = CircleFactory.random()
    """

    # List of all sprite filenames (no extension needed)
    _NAMES = [
        "circle_white_36",
        "circle_white_38",
        "circle_white_40",
        "circle_white_42",
        "circle_white_44",
        "circle_white_46",
        "circle_white_48",
        "circle_white_50",
        "circle_white_52",
        "circle_white_54",
        "circle_white_56",
        "circle_white_58",
        "circle_white_60",
        "circle_white_62",
        "circle_white_64",
        "circle_white_66",
        "circle_white_68",
        "circle_white_70",
        "circle_white_72",
        "circle_white_74",
        "circle_white_76",
        "circle_white_78",
        "circle_white_80",
        "circle_white_82",
        "circle_white_84",
        "circle_white_86",
        "circle_white_88",
        "circle_white_90",
        "circle_white_92",
        "circle_white_94",
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
