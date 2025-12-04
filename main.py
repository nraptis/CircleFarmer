# main.py  (updated top-row padding)

from __future__ import annotations

import sys
from pixel_bag import PixelBag
from random import random

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
)
from PySide6.QtCore import QSize

from home_view import HomeView
from top_panel import TopPanel
from left_panel import LeftPanel
from right_panel import RightPanel


class MainWindow(QMainWindow):
    """
    Layout:
        [  32px top padding  ]
        [ 16px L | LeftPanel | TopPanel | RightPanel | 16px R ]
        [                HomeView (fills)                  ]
    """

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Data Spoofer")
        self.resize(QSize(1024, 768))

        # --------------------------------------------------
        # Central container
        # --------------------------------------------------
        central = QWidget(self)
        self.setCentralWidget(central)

        root_layout = QVBoxLayout(central)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # --------------------------------------------------
        # TOP ROW + PADDING CONTAINER
        # --------------------------------------------------
        top_container = QWidget(central)
        top_container_layout = QHBoxLayout(top_container)

        # padding: top=32, left=16, bottom=0, right=16
        top_container_layout.setContentsMargins(16, 32, 16, 0)
        top_container_layout.setSpacing(0)

        # The actual row with the 3 panels (no inner margins)
        top_row = QHBoxLayout()
        top_row.setContentsMargins(0, 0, 0, 0)
        top_row.setSpacing(0)

        # Panels
        self.left_panel = LeftPanel(top_container)
        self.top_panel = TopPanel(top_container)
        self.right_panel = RightPanel(top_container)

        top_row.addWidget(self.left_panel)
        top_row.addWidget(self.top_panel, 1)   # center expands
        top_row.addWidget(self.right_panel)

        # Add row into padded container
        top_container_layout.addLayout(top_row)

        # Add padded container to root layout
        root_layout.addWidget(top_container)

        # --------------------------------------------------
        # BOTTOM CONTENT (HOME VIEW)
        # --------------------------------------------------
        self.home_view = HomeView(central)
        root_layout.addWidget(self.home_view, 1)  # stretch to fill



        # ---------------------------------------
        # Create PixelBag + 25 random pixels
        # ---------------------------------------
        bag = PixelBag()

        y = 1
        x = 2
        for _ in range(25):

            x += 2
            if x > 10:
                x = 2
                y += 1
            bag.add(x, y)

        # ---------------------------------------
        # Convert to JSON
        # ---------------------------------------
        j = bag.to_json()
        print("JSON:")
        print(j)

        # ---------------------------------------
        # Convert back from JSON
        # ---------------------------------------
        bag2 = PixelBag.from_json(j)

        print("\nBag2:", len(bag2), sorted(list(bag2)))
        print("Bag :", len(bag),  sorted(list(bag)))
        


def main() -> None:
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
