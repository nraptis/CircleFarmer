from __future__ import annotations
import random
from bitmap import Bitmap
from file_utils import FileUtils
from PIL import Image

class BackgroundFactory:
    """
    Provides random background Bitmaps from the local resources folder.
    All images expected under:
        /images/backgrounds/
    """

    # dish_00 ... dish_32
    _NAMES = [f"dish_{i:02d}" for i in range(33)]

    _SUBDIR = "/images/backgrounds/"
    _EXT = ".png"

    @classmethod
    def random(cls) -> Bitmap:
        """
        Load a random dish image, apply random transforms
        (rotation, flips, resize), and return as a Bitmap.
        """

        # ------------------------------------------------------
        # 1. Choose random file and load Pillow image
        # ------------------------------------------------------
        name = random.choice(cls._NAMES)
        full_name = name + cls._EXT

        pil = FileUtils.load_local_image(
            subdirectory=cls._SUBDIR,
            name="/" + full_name,
        )

        # ------------------------------------------------------
        # 2. Random ROTATION (0, 90, 180, 270 degrees)
        # ------------------------------------------------------
        rotate_choice = random.randint(0, 3)   # avoids identity 4
        angle = rotate_choice * 90
        if angle != 0:
            pil = pil.rotate(angle, expand=True)

        # ------------------------------------------------------
        # 3. Random FLIPS
        # ------------------------------------------------------
        if random.random() < 0.5:
            pil = pil.transpose(Image.FLIP_LEFT_RIGHT)

        if random.random() < 0.5:
            pil = pil.transpose(Image.FLIP_TOP_BOTTOM)

        # ------------------------------------------------------
        # 4. Random RESIZE (square, 500–900 px)
        # ------------------------------------------------------
        new_size = random.randint(500, 900)
        pil = pil.resize((new_size, new_size), Image.BILINEAR)

        # ------------------------------------------------------
        # 5. Convert to Bitmap and return
        # ------------------------------------------------------
        bmp = Bitmap()
        bmp.import_pillow(pil)
        return bmp
