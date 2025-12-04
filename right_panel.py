# right_panel.py
from __future__ import annotations

from PySide6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QLabel
from PySide6.QtCore import Qt


class RightPanel(QWidget):
    """
    Right side panel, fixed width 256.

    Data rows:
      1. Target count min   (default "4")
      2. Target count max   (default "10")
      3. Max overlap        (default "2")
      4. Maximum tries      (default "100")
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

        # Row 1: Target count min
        self.target_min_edit = QLineEdit(self)
        self.target_min_edit.setText("4")
        form.addRow(QLabel("Target count min:", self), self.target_min_edit)

        # Row 2: Target count max
        self.target_max_edit = QLineEdit(self)
        self.target_max_edit.setText("10")
        form.addRow(QLabel("Target count max:", self), self.target_max_edit)

        # Row 3: Max overlap
        self.max_overlap_edit = QLineEdit(self)
        self.max_overlap_edit.setText("2")
        form.addRow(QLabel("Max overlap:", self), self.max_overlap_edit)

        # Row 4: Maximum tries
        self.max_tries_edit = QLineEdit(self)
        self.max_tries_edit.setText("100")
        form.addRow(QLabel("Maximum tries:", self), self.max_tries_edit)

        main_layout.addLayout(form)
        main_layout.addStretch(1)

    # Optional convenience getters

    def target_min(self) -> int:
        return int(self.target_min_edit.text() or 0)

    def target_max(self) -> int:
        return int(self.target_max_edit.text() or 0)

    def max_overlap(self) -> int:
        return int(self.max_overlap_edit.text() or 0)

    def max_tries(self) -> int:
        return int(self.max_tries_edit.text() or 0)
