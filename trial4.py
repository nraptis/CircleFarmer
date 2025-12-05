# trial4.py
from __future__ import annotations

import json
from PIL import Image

from file_utils import FileUtils
from image_annotation_document import ImageAnnotationDocument


def trial4() -> None:
    """
    Pillow-only verification trial:

    - Load a generated image and its annotation JSON.
    - Use Pillow pixel ops to:
        * paint black onto every annotated pixel on a copy of the image
        * build a pure mask (black background, white where annotated)
    """

    # --------------------------------------------------
    # 1. Choose which sample to inspect
    #    Adjust to match what Runner generated.
    # --------------------------------------------------
    folder = "testing"  # or "training"
    base_name = "genxyz_test_00008"

    image_file_name = base_name
    annotation_file_name = f"{base_name}_annotations"

    # --------------------------------------------------
    # 2. Load original image as Pillow Image (RGBA)
    # --------------------------------------------------
    pil_img = FileUtils.load_local_image(
        subdirectory=f"/{folder}/",
        name=f"/{image_file_name}",
        extension="png",
    )
    pil_img = pil_img.convert("RGBA")

    w, h = pil_img.size

    # Copy for overlay
    overlay = pil_img.copy()
    overlay_px = overlay.load()

    # Mask: single-channel L (0=black, 255=white)
    mask = Image.new("L", (w, h), 0)
    mask_px = mask.load()

    # --------------------------------------------------
    # 3. Load annotation JSON and rebuild document
    # --------------------------------------------------
    anno_text = FileUtils.load_local_text(
        subdirectory=f"/{folder}/",
        name=f"/{annotation_file_name}",
        extension="json",
        encoding="utf-8",
    )

    anno_json = json.loads(anno_text)
    doc = ImageAnnotationDocument.from_json(anno_json)

    # Assuming doc.data is a DataLabelCollection with .labels
    data_collection = doc.data
    labels = getattr(data_collection, "labels", data_collection)

    # --------------------------------------------------
    # 4. Paint black on overlay and white on mask
    # --------------------------------------------------
    for data_label in labels:
        bag = data_label.pixel_bag
        for (x, y) in bag:
            if 0 <= x < w and 0 <= y < h:
                r, g, b, a = overlay_px[x, y]
                # black, keep alpha
                overlay_px[x, y] = (0, 0, 0, a)
                # white in mask
                mask_px[x, y] = 255

    # --------------------------------------------------
    # 5. Save Pillow-generated overlay and mask
    # --------------------------------------------------
    overlay_name = f"TEST{base_name}_overlay_pil"
    mask_name = f"TEST{base_name}_mask_pil"

    FileUtils.save_local_image(
        overlay,
        folder,
        overlay_name,
        "png",
    )

    FileUtils.save_local_image(
        mask,
        folder,
        mask_name,
        "png",
    )

    print(f"trial4: wrote {overlay_name}.png and {mask_name}.png in '{folder}'")


if __name__ == "__main__":
    trial4()
