# trial3.py
from __future__ import annotations

import json

from bitmap import Bitmap
from rgba import RGBA
from file_utils import FileUtils
from image_annotation_document import ImageAnnotationDocument


def trial3() -> None:
    """
    Debug / visualization trial:

    - Load a generated image and its annotation JSON.
    - Paint black onto every annotated pixel on a copy of the image.
    - Build a pure mask image with white where annotated, black elsewhere.
    - Save both images.
    """

    # --------------------------------------------------
    # 1. Choose which sample to inspect
    #    (adjust these to match what Runner generated)
    # --------------------------------------------------
    folder = "testing"  # or "training"
    base_name = "genxyz_test_00000"  # e.g. same pattern as Runner

    image_file_name = base_name
    annotation_file_name = f"{base_name}_annotations"

    # --------------------------------------------------
    # 2. Load the original image into a Bitmap
    # --------------------------------------------------
    pil_image = FileUtils.load_local_image(
        subdirectory=f"/{folder}/",
        name=f"/{image_file_name}",
        extension="png",
    )

    original = Bitmap()
    original.import_pillow(pil_image)

    # We'll work on a copy so we keep original untouched if needed
    overlay = Bitmap(original.width, original.height)
    overlay.set_size(original.width, original.height)
    for x in range(original.width):
        for y in range(original.height):
            overlay.rgba[x][y] = original.rgba[x][y]

    # --------------------------------------------------
    # 3. Load annotation JSON and rebuild the document
    # --------------------------------------------------
    anno_text = FileUtils.load_local_text(
        subdirectory=f"/{folder}/",
        name=f"/{annotation_file_name}",
        extension="json",
        encoding="utf-8",
    )

    anno_json = json.loads(anno_text)
    doc = ImageAnnotationDocument.from_json(anno_json)

    # --------------------------------------------------
    # 4. Build a pure mask image (black bg, white where annotated)
    # --------------------------------------------------
    mask = Bitmap(original.width, original.height)
    mask.set_size(original.width, original.height)
    # default is black with full alpha already via Bitmap.set_size

    width = original.width
    height = original.height

    # Depending on your ImageAnnotationDocument, adjust how to get labels.
    # Here we assume `doc.data` is a DataLabelCollection and has `.labels`.
    data_collection = doc.data
    labels = getattr(data_collection, "labels", data_collection)

    # --------------------------------------------------
    # 5. Paint black on overlay, white on mask for each annotated pixel
    # --------------------------------------------------
    for data_label in labels:
        bag = data_label.pixel_bag
        for (x, y) in bag:
            if 0 <= x < width and 0 <= y < height:
                # Black on overlay, preserving alpha from original
                orig_px = overlay.rgba[x][y]
                overlay.rgba[x][y] = RGBA(0, 0, 0, orig_px.ai)

                # White in mask (fully opaque)
                mask.rgba[x][y] = RGBA(255, 255, 255, 255)

    # --------------------------------------------------
    # 6. Save overlay + mask images
    # --------------------------------------------------
    overlay_name = f"TEST{base_name}_overlay"
    mask_name = f"TEST{base_name}_mask"

    FileUtils.save_local_image(
        overlay.export_pillow(),
        folder,
        overlay_name,
        "png",
    )

    FileUtils.save_local_image(
        mask.export_pillow(),
        folder,
        mask_name,
        "png",
    )

    print(f"trial3: wrote overlay and mask for {base_name} in folder '{folder}'")


if __name__ == "__main__":
    trial3()
