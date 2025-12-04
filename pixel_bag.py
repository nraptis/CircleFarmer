# pixel_bag.py
from __future__ import annotations

from typing import Any, Dict

from pixel_bag_run_length import PixelBagRunLength
from pixel_bag_run_length_stripe import PixelBagRunLengthStripe


class PixelBag:
    """
    Stores a set of (x, y) integer pixel positions.
    Does not store duplicates (internally a set),
    but add/remove semantics allow double-add and remove-nonexistent
    without raising exceptions.
    """

    def __init__(self) -> None:
        self._set = set()   # stores (x, y)

    # --------------------------------------------------
    # Basic operations
    # --------------------------------------------------
    def clear(self) -> None:
        self._set.clear()

    def add(self, x: int, y: int) -> None:
        """Add a pixel. Adding an existing pixel is allowed and ignored."""
        self._set.add((int(x), int(y)))

    def remove(self, x: int, y: int) -> None:
        """Remove a pixel. Removing a missing pixel is allowed and ignored."""
        self._set.discard((int(x), int(y)))  # discard() never raises

    def contains(self, x: int, y: int) -> bool:
        """Check if a pixel exists in the bag."""
        return (int(x), int(y)) in self._set

    # --------------------------------------------------
    # Bounding box helpers
    # --------------------------------------------------
    @property
    def xmin(self):
        if not self._set:
            return None
        return min(px for (px, _) in self._set)

    @property
    def xmax(self):
        if not self._set:
            return None
        return max(px for (px, _) in self._set)

    @property
    def ymin(self):
        if not self._set:
            return None
        return min(py for (_, py) in self._set)

    @property
    def ymax(self):
        if not self._set:
            return None
        return max(py for (_, py) in self._set)

    # --------------------------------------------------
    # Ranges for easy looping
    # --------------------------------------------------
    def xrange(self):
        """
        Return range(xmin, xmax+1).
        If empty, return range(0).
        """
        if not self._set:
            return range(0)
        return range(self.xmin, self.xmax + 1)

    def yrange(self):
        """
        Return range(ymin, ymax+1).
        If empty, return range(0).
        """
        if not self._set:
            return range(0)
        return range(self.ymin, self.ymax + 1)

    # --------------------------------------------------
    # Utility
    # --------------------------------------------------
    def __len__(self):
        return len(self._set)

    def __iter__(self):
        """Iterate over (x, y) pairs."""
        return iter(self._set)

    def __repr__(self):
        return f"PixelBag({len(self._set)} pixels)"

    # --------------------------------------------------
    # Run-length conversion
    # --------------------------------------------------
    def to_run_length(self) -> "PixelBagRunLength":
        result = PixelBagRunLength()

        _xmin = self.xmin
        _xmax = self.xmax
        if _xmin is None or _xmax is None:
            return result

        for y in self.yrange():
            x = _xmin
            while x <= _xmax:
                if self.contains(x, y):
                    x_start = x
                    x_end = x
                    x += 1
                    while x <= _xmax and self.contains(x, y):
                        x_end = x
                        x += 1
                    result.add_stripe(PixelBagRunLengthStripe(y, x_start, x_end))
                else:
                    x += 1

        return result

    # --------------------------------------------------
    # JSON serialization
    # --------------------------------------------------
    def to_json(self) -> Dict[str, Any]:
        """
        Serialize this PixelBag to a JSON-compatible dict.

        Currently uses run-length encoding under the hood, so the JSON
        format is exactly whatever PixelBagRunLength.to_json() returns:
            { "stripes": [ { "y": ..., "x_start": ..., "x_end": ... }, ... ] }
        """
        rle = self.to_run_length()
        return rle.to_json()

    @staticmethod
    def from_json(data: Dict[str, Any]) -> "PixelBag":
        """
        Deserialize a PixelBag from a JSON-compatible dict produced
        by PixelBag.to_json().

        Reconstructs all (x, y) pixels from the run-length stripes.
        """
        rle = PixelBagRunLength.from_json(data)
        bag = PixelBag()

        for stripe in rle.stripes:
            y = stripe.y
            for x in range(stripe.x_start, stripe.x_end + 1):
                bag.add(x, y)

        return bag
