# middle_left_panel.py
from __future__ import annotations

from PySide6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QLabel
from PySide6.QtCore import Qt


class MiddleLeftPanel(QWidget):
    """
    Middle-left panel, fixed width 256.

    Data rows:
      1. output width   (default "256")
      2. output height  (default "256")
      3. start index    (default "0")
      4. end index      (default "8")
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

        # Row 1: output width
        self.output_width_edit = QLineEdit(self)
        self.output_width_edit.setText("256")
        form.addRow(QLabel("output width:", self), self.output_width_edit)

        # Row 2: output height
        self.output_height_edit = QLineEdit(self)
        self.output_height_edit.setText("256")
        form.addRow(QLabel("output height:", self), self.output_height_edit)

        # Row 3: start index
        self.start_index_edit = QLineEdit(self)
        self.start_index_edit.setText("0")
        form.addRow(QLabel("start index:", self), self.start_index_edit)

        # Row 4: end index
        self.end_index_edit = QLineEdit(self)
        self.end_index_edit.setText("600")
        form.addRow(QLabel("end index:", self), self.end_index_edit)

        main_layout.addLayout(form)
        main_layout.addStretch(1)

    # --------------------------------------------------
    # Convenience getters
    # --------------------------------------------------
    def output_width(self) -> int:
        return int(self.output_width_edit.text() or 0)

    def output_height(self) -> int:
        return int(self.output_height_edit.text() or 0)

    def start_index(self) -> int:
        return int(self.start_index_edit.text() or 0)

    def end_index(self) -> int:
        return int(self.end_index_edit.text() or 0)
