# pixel_bag_run_length.py
from __future__ import annotations
from typing import Any, List

from pixel_bag_run_length_stripe import PixelBagRunLengthStripe


class PixelBagRunLength:
    """
    Run-length representation of a PixelBag:
    a list of horizontal stripes.
    """

    def __init__(self, stripes: List[PixelBagRunLengthStripe] | None = None) -> None:
        self.stripes: List[PixelBagRunLengthStripe] = stripes or []

    # --------------------------------------------------
    # JSON serialization
    # --------------------------------------------------
    def to_json(self) -> List[Any]:
        """
        Serialize to a JSON-compatible list of objects:
            [ { y, x_start, x_end }, ... ]
        """
        return [stripe.to_json() for stripe in self.stripes]

    @staticmethod
    def from_json(data: List[Any]) -> "PixelBagRunLength":
        """
        Deserialize from:
            [ { y, x_start, x_end }, ... ]
        """
        stripes = [
            PixelBagRunLengthStripe.from_json(item)
            for item in data
        ]
        return PixelBagRunLength(stripes=stripes)

    # --------------------------------------------------
    # Utility
    # --------------------------------------------------
    def add_stripe(self, stripe: PixelBagRunLengthStripe) -> None:
        self.stripes.append(stripe)

    def __len__(self) -> int:
        return len(self.stripes)

    def __iter__(self):
        return iter(self.stripes)

    def __repr__(self) -> str:
        return f"PixelBagRunLength({len(self.stripes)} stripes)"
