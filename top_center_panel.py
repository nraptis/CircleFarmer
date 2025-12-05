# top_center_panel.py
from __future__ import annotations

from PySide6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QLabel
from PySide6.QtCore import Qt


class TopCenterPanel(QWidget):
    """
    Center top panel, fixed width 256.

    Data rows:
      1. File name base      (default: "my_model")
      2. Training postfix    (default: "training")
      3. Testing postfix     (default: "testing")
      4. Leading zeros       (default: "5")
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

        # Row 1: file name base
        self.file_name_base_edit = QLineEdit(self)
        self.file_name_base_edit.setText("proto_cells")
        form.addRow(QLabel("File name base:", self), self.file_name_base_edit)

        # Row 2: training postfix
        self.training_postfix_edit = QLineEdit(self)
        self.training_postfix_edit.setText("train")
        form.addRow(QLabel("Training postfix:", self), self.training_postfix_edit)

        # Row 3: testing postfix
        self.testing_postfix_edit = QLineEdit(self)
        self.testing_postfix_edit.setText("test")
        form.addRow(QLabel("Testing postfix:", self), self.testing_postfix_edit)

        # Row 4: leading zeros
        self.leading_zeros_edit = QLineEdit(self)
        self.leading_zeros_edit.setText("3")
        form.addRow(QLabel("Leading zeros:", self), self.leading_zeros_edit)

        main_layout.addLayout(form)
        main_layout.addStretch(1)

    # Convenience accessors

    def file_name_base(self) -> str:
        return self.file_name_base_edit.text().strip()

    def training_postfix(self) -> str:
        return self.training_postfix_edit.text().strip()

    def testing_postfix(self) -> str:
        return self.testing_postfix_edit.text().strip()

    def leading_zeros(self) -> str:
        return self.leading_zeros_edit.text().strip()
