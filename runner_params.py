# runner_params.py
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RunnerParams:
    """
    Immutable snapshot of all user-entered settings from the panels.
    """

    # TopLeftPanel (alpha / color parameters)
    alpha_min: float
    alpha_max: float
    alpha_noise: float
    color_noise: float

    # TopCenterPanel (file naming)
    file_name_base: str
    training_postfix: str
    testing_postfix: str
    leading_zeros: int  # how many digits to pad with

    # TopRightPanel (target / overlap constraints)
    target_min: int
    target_max: int
    max_overlap: int
    max_tries: int

    # MiddleLeftPanel (output + index range)
    output_width: int
    output_height: int
    start_index: int
    end_index: int

    def validate(self) -> None:
        """
        Sanity checks. Raise ValueError if something is obviously invalid.
        """
        if self.alpha_min < 0.0 or self.alpha_max > 1.0:
            raise ValueError("alpha_min/alpha_max should be between 0.0 and 1.0")

        if self.alpha_min > self.alpha_max:
            raise ValueError("alpha_min cannot be greater than alpha_max")

        if self.target_min < 0 or self.target_max < 0:
            raise ValueError("target_min/target_max must be non-negative")

        if self.target_min > self.target_max:
            raise ValueError("target_min cannot be greater than target_max")

        if self.leading_zeros < 0:
            raise ValueError("leading_zeros cannot be negative")

        if self.max_overlap < 0:
            raise ValueError("max_overlap cannot be negative")

        if self.max_tries <= 0:
            raise ValueError("max_tries must be positive")

        if self.output_width <= 0 or self.output_height <= 0:
            raise ValueError("output_width/output_height must be positive")

        if self.start_index < 0:
            raise ValueError("start_index must be >= 0")

        if self.end_index < self.start_index:
            raise ValueError("end_index must be >= start_index")
