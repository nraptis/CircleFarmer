# home_view.py
from __future__ import annotations

from PySide6.QtWidgets import QWidget, QPushButton, QGridLayout
from PySide6.QtCore import QSize, Qt


class HomeView(QWidget):
    """
    Main content view for the app.

    Contains two buttons:
      - 'Generate Test' pinned to the top-left.
      - 'Generate Train' pinned to the bottom-right.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._setup_ui()
        self._connect_signals()

    # ------------------------------------------------------------------
    # UI Setup
    # ------------------------------------------------------------------
    def _setup_ui(self) -> None:
        # Create buttons
        self.generate_test_button = QPushButton("Generate Test")
        self.generate_train_button = QPushButton("Generate Train")

        # Size: 160 x 66, rounded rectangle look via stylesheet
        for button in (self.generate_test_button, self.generate_train_button):
            button.setFixedSize(QSize(160, 66))
            button.setStyleSheet(
                """
                QPushButton {
                    border-radius: 16px;
                    border: 1px solid #444;
                    padding: 8px 16px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    border: 1px solid #666;
                }
                QPushButton:pressed {
                    border: 1px solid #222;
                }
                """
            )

        layout = QGridLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(0)

        # Top-left corner
        layout.addWidget(
            self.generate_test_button,
            0,
            0,
            alignment=Qt.AlignTop | Qt.AlignLeft,
        )

        # Bottom-right corner
        layout.addWidget(
            self.generate_train_button,
            2,
            2,
            alignment=Qt.AlignBottom | Qt.AlignRight,
        )

        layout.setRowStretch(1, 1)
        layout.setColumnStretch(1, 1)

        self.setLayout(layout)

    # ------------------------------------------------------------------
    # Signal connections
    # ------------------------------------------------------------------
    def _connect_signals(self) -> None:
        self.generate_test_button.clicked.connect(self.on_generate_test_clicked)
        self.generate_train_button.clicked.connect(self.on_generate_train_clicked)

    # ------------------------------------------------------------------
    # Slots / callbacks
    # ------------------------------------------------------------------
    def on_generate_test_clicked(self) -> None:
        print("Generate Test was clicked")

    def on_generate_train_clicked(self) -> None:
        print("Generate Train was clicked")
