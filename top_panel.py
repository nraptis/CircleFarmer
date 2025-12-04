# top_panel.py
from __future__ import annotations

from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QLabel,
)
from PySide6.QtCore import Qt


class TopPanelCenterBox(QWidget):
    """
    Centered box inside the top panel.

    Fixed width: 256 px
    Same height as TopPanel (layout-managed vertically).

    Contains 4 data rows:
      1. File name base      (default: "my_model")
      2. Training postfix    (default: "training")
      3. Testing postfix     (default: "testing")
      4. Leading zeros       (default: "5")
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.setFixedWidth(256)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(4)

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)
        form.setFormAlignment(Qt.AlignCenter)
        form.setContentsMargins(0, 0, 0, 0)
        form.setSpacing(4)

        # Row 1: file name base
        self.file_name_base_edit = QLineEdit(self)
        self.file_name_base_edit.setText("my_model")
        form.addRow(QLabel("File name base:", self), self.file_name_base_edit)

        # Row 2: training postfix
        self.training_postfix_edit = QLineEdit(self)
        self.training_postfix_edit.setText("training")
        form.addRow(QLabel("Training postfix:", self), self.training_postfix_edit)

        # Row 3: testing postfix
        self.testing_postfix_edit = QLineEdit(self)
        self.testing_postfix_edit.setText("testing")
        form.addRow(QLabel("Testing postfix:", self), self.testing_postfix_edit)

        # Row 4: leading zeros
        self.leading_zeros_edit = QLineEdit(self)
        self.leading_zeros_edit.setText("5")
        form.addRow(QLabel("Leading zeros:", self), self.leading_zeros_edit)

        main_layout.addLayout(form)
        main_layout.addStretch(1)

    # Convenience accessors if you want them:

    def file_name_base(self) -> str:
        return self.file_name_base_edit.text().strip()

    def training_postfix(self) -> str:
        return self.training_postfix_edit.text().strip()

    def testing_postfix(self) -> str:
        return self.testing_postfix_edit.text().strip()

    def leading_zeros(self) -> str:
        return self.leading_zeros_edit.text().strip()


class TopPanel(QWidget):
    """
    Top panel widget.

    Hosts a centered TopPanelCenterBox that is 256 px wide,
    with flexible space on the left and right.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addStretch(1)

        self.center_box = TopPanelCenterBox(self)
        layout.addWidget(self.center_box)

        layout.addStretch(1)
