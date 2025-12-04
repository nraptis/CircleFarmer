# main.py
from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QSize

from home_view import HomeView
from file_utils import FileUtils

from rgba import RGBA
from bitmap import Bitmap

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


        # ----------------------------------------------------------
        # 1. Load image using FileUtils (as bytes) → Pillow Image
        # ----------------------------------------------------------

        image = FileUtils.load_local_image(subdirectory="images", name="sample_256_256", extension="png")

        # ----------------------------------------------------------
        # 2. Convert Pillow → Bitmap
        # ----------------------------------------------------------
        bmp = Bitmap()
        bmp.import_pillow(image)

        # ----------------------------------------------------------
        # 3. Print selected pixels
        # ----------------------------------------------------------
        coords = [
            (0, 0),
            (1, 1),
            (25, 0),
            (0, 25),
            (255, 255),
        ]

        for (x, y) in coords:
            px = bmp.rgba[x][y]
            print(f"Pixel ({x},{y}): {px}")

        for r in bmp.rgba:
            for a in r:
                a.af /= 2.0
                a.rf *= 1.5

        out = bmp.export_pillow()

        FileUtils.save_local_image(out, name="ff/junk.png")


        # will crash, loses "images" from path
        canvas = Bitmap.with_local_image(name="images/sample_256_256", extension="png")
        glyph = Bitmap.with_local_image(name="/images/circles/circle_black_56.png")

        canvas.stamp(glyph, 0 - 16, 0 - 16)

        FileUtils.save_local_image(canvas.export_pillow(), subdirectory="aaa", name="glyphed1", extension="png")
        
        canvas.stamp(glyph, 256 - 32, 0 - 12)
        
        FileUtils.save_local_image(canvas.export_pillow(), subdirectory="aaa", name="glyphed2", extension="png")
        
        canvas.stamp(glyph, -10, 256 - 30)
        FileUtils.save_local_image(canvas.export_pillow(), subdirectory="aaa", name="glyphed3", extension="png")

        canvas.stamp(glyph, 236, 220)
        FileUtils.save_local_image(canvas.export_pillow(), subdirectory="aaa", name="glyphed4", extension="png")
        

        canvas.stamp_alpha(glyph, 100, 100)
        FileUtils.save_local_image(canvas.export_pillow(), subdirectory="aaa", name="glyphed5", extension="png")
        


        base_dir = "/Users/naraptis/Desktop/CircleFarmer/images"
        stamps_dir = f"{base_dir}/test_stamps"

        # --------------------------------------------------
        # Canvas
        # --------------------------------------------------
        canvas = Bitmap.with_image(f"{base_dir}/sample_768_812.png")

        # --------------------------------------------------
        # Glyphs with different alphas
        # --------------------------------------------------
        glyph_paths = [
            f"{stamps_dir}/alpha_25.png",
            f"{stamps_dir}/alpha_50.png",
            f"{stamps_dir}/alpha_75.png",
            f"{stamps_dir}/alpha_100.png",
        ]
        glyphs = [Bitmap.with_image(path) for path in glyph_paths]

        # --------------------------------------------------
        # Layout parameters
        # --------------------------------------------------
        start_x = 150
        start_y = 150
        step_x = 100
        step_y = 100

        # 4 rows:
        #   0: plain stamp (overwrite)
        #   1: alpha blend
        #   2: premultiplied blend
        #   3: additive blend
        modes = ["stamp", "alpha", "premult", "additive"]

        for row_index, mode in enumerate(modes):
            y = start_y + row_index * step_y

            for col_index, glyph in enumerate(glyphs):
                x = start_x + col_index * step_x

                if mode == "stamp":
                    canvas.stamp(glyph, x, y)
                elif mode == "alpha":
                    canvas.stamp_alpha(glyph, x, y)
                elif mode == "premult":
                    canvas.stamp_premultiplied(glyph, x, y)
                elif mode == "additive":
                    canvas.stamp_additive(glyph, x, y)

        # --------------------------------------------------
        # Save result
        # --------------------------------------------------
        out_image = canvas.export_pillow()
        FileUtils.save_image(out_image, f"{stamps_dir}/stamp_blends_grid.png")

        

        

        


def main() -> None:
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
