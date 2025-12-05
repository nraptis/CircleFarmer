# circle_label_placement.py
from __future__ import annotations

from dataclasses import dataclass
from labels.data_label import DataLabel

@dataclass
class CircleLabelPlacement:
    data_label: DataLabel
    center_x: int
    center_y: int
    radius: float

    def intersects(self, x: int, y: int, radius: float) -> bool:
        """
        Return True if this circle intersects another circle whose center
        is at (x, y) with the given radius.
        Uses distance-squared check to avoid sqrt.
        """
        dx = self.center_x - x
        dy = self.center_y - y

        dist_sq = dx * dx + dy * dy
        sum_r = self.radius + radius
        sum_r_sq = sum_r * sum_r

        return dist_sq <= sum_r_sq
