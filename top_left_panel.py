# top_left_panel.py
from __future__ import annotations

from PySide6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QLabel
from PySide6.QtCore import Qt


class TopLeftPanel(QWidget):
    """
    Top-left side panel, fixed width 256.

    Data rows:
      1. alpha min     (default "0.25")
      2. alpha max     (default "0.75")
      3. alpha noise   (default "0.1")
      4. color noise   (default "0.1")
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.setFixedWidth(256)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(4)

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)
        form.setFormAlignment(Qt.AlignTop | Qt.AlignLeft)
        form.setContentsMargins(0, 0, 0, 0)
        form.setSpacing(4)

        # Row 1: alpha min
        self.alpha_min_edit = QLineEdit(self)
        self.alpha_min_edit.setText("0.65")
        form.addRow(QLabel("alpha min:", self), self.alpha_min_edit)

        # Row 2: alpha max
        self.alpha_max_edit = QLineEdit(self)
        self.alpha_max_edit.setText("0.85")
        form.addRow(QLabel("alpha max:", self), self.alpha_max_edit)

        # Row 3: alpha noise
        self.alpha_noise_edit = QLineEdit(self)
        self.alpha_noise_edit.setText("0.10")
        form.addRow(QLabel("alpha noise:", self), self.alpha_noise_edit)

        # Row 4: color noise
        self.color_noise_edit = QLineEdit(self)
        self.color_noise_edit.setText("0.25")
        form.addRow(QLabel("color noise:", self), self.color_noise_edit)

        main_layout.addLayout(form)
        main_layout.addStretch(1)

    # Optional convenience getters

    def alpha_min(self) -> float:
        return float(self.alpha_min_edit.text() or 0.0)

    def alpha_max(self) -> float:
        return float(self.alpha_max_edit.text() or 0.0)

    def alpha_noise(self) -> float:
        return float(self.alpha_noise_edit.text() or 0.0)

    def color_noise(self) -> float:
        return float(self.color_noise_edit.text() or 0.0)
