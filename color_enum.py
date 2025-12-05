from __future__ import annotations
import random
from enum import Enum, auto
from image.rgba import RGBA

INSET = 32            # avoid pure 0 or 255
MAXC  = 255 - INSET   # 223


class ColorName(Enum):
    RED     = auto()
    YELLOW  = auto()
    GREEN   = auto()
    CYAN    = auto()
    BLUE    = auto()
    MAGENTA = auto()

    # --------------------------------------------------
    # Class method: random color from first num_colors
    # --------------------------------------------------
    @classmethod
    def random(cls, num_colors: int) -> "ColorName":
        """
        Choose a random color from the first `num_colors` colors in the
        predefined order:

            RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA

        If num_colors < 1 → uses only RED.
        If num_colors > 6 → clamps to 6.
        """
        ordered = [
            cls.RED,
            cls.GREEN,
            cls.BLUE,
            cls.YELLOW,
            cls.CYAN,
            cls.MAGENTA,
        ]

        if num_colors < 1:
            num_colors = 1
        if num_colors > len(ordered):
            num_colors = len(ordered)

        pool = ordered[:num_colors]
        return random.choice(pool)

    # --------------------------------------------------
    # Human-readable label
    # --------------------------------------------------
    def label(self) -> str:
        return self.name.capitalize()

    # --------------------------------------------------
    # Baseline RGB tuple (no alpha)
    # --------------------------------------------------
    def rgb_tuple(self) -> tuple[int, int, int]:
        match self:
            case ColorName.RED:
                return (MAXC, INSET, INSET)
            case ColorName.YELLOW:
                return (MAXC, MAXC, INSET)
            case ColorName.GREEN:
                return (INSET, MAXC, INSET)
            case ColorName.CYAN:
                return (INSET, MAXC, MAXC)
            case ColorName.BLUE:
                return (INSET, INSET, MAXC)
            case ColorName.MAGENTA:
                return (MAXC, INSET, MAXC)
        raise ValueError("Unknown ColorName")

    def rgba(self) -> RGBA:
        r, g, b = self.rgb_tuple()
        return RGBA(r, g, b, 255)

    def __str__(self) -> str:
        return f"{self.label()} {self.rgb_tuple()}"
