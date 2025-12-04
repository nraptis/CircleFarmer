# main.py
from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QSize

from home_view import HomeView
from file_utils import FileUtils

class MainWindow(QMainWindow):
    """
    Main application window.

    Hosts HomeView as its central widget.
    """

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Data Spoofer")
        # Initial size: 1024 x 768; window remains resizable.
        self.resize(QSize(1024, 768))


        # Load the sample image
        img = FileUtils.load_local_image(
            subdirectory="images",
            name="sample_256_256",
            extension="png"
        )

        # Rotate 90 degrees (Pillow rotates counterclockwise by default)
        rotated = img.rotate(90, expand=True)

        # Save result
        FileUtils.save_local_image(
            rotated,
            subdirectory="output",
            name="test",
            extension="png"
        )
        

        # ---------------------------------------------------------
        # 1. Load the text as a string (caller must specify encoding)
        # ---------------------------------------------------------
        src_path = "/Users/naraptis/Desktop/CircleFarmer/text/hello.txt"

        text = FileUtils.load_text(
            file_path=src_path,
            encoding="utf-8"
        )

        # ---------------------------------------------------------
        # 2. Capitalize the string
        # ---------------------------------------------------------
        capitalized = text.upper()

        # ---------------------------------------------------------
        # 3. Save UTF-8 → output/test_utf_8.tst
        # ---------------------------------------------------------
        FileUtils.save_local_text(
            text=capitalized,
            subdirectory="output",
            name="test_utf_8",
            extension="txt",
            encoding="utf-8",
        )

        # ---------------------------------------------------------
        # 4. Add a heart emoji, save UTF-16 → output/test_utf_16.tst
        # ---------------------------------------------------------
        with_heart = capitalized + " ❤️"

        FileUtils.save_local_text(
            text=with_heart,
            subdirectory="output",
            name="test_utf_16",
            extension="txt",
            encoding="utf-16",
        )


def main() -> None:
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
