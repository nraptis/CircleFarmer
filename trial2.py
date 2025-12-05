from data_label import DataLabel
from pixel_bag import PixelBag
from data_label_collection import DataLabelCollection
from image_annotation_document import ImageAnnotationDocument
import random


def make_block_bag(x0: int, y0: int, w: int, h: int) -> PixelBag:
    """Helper to build a rectangular block of pixels."""
    bag = PixelBag()
    for x in range(x0, x0 + w):
        for y in range(y0, y0 + h):
            bag.add(x, y)
    return bag


def random_bag() -> PixelBag:
    """Random rectangle with 8–20 pixels."""
    x0 = random.randint(0, 200)
    y0 = random.randint(0, 200)
    w = random.randint(2, 6)     # 2–6 wide
    h = random.randint(2, 6)     # 2–6 tall
    return make_block_bag(x0, y0, w, h)


def build_test_collection() -> DataLabelCollection:
    labels = []

    # 4-banger
    for _ in range(4):
        labels.append(DataLabel("Quadrocyte", random_bag()))

    # 2 triplicates
    for _ in range(3):
        labels.append(DataLabel("TripAcyte", random_bag()))
    for _ in range(3):
        labels.append(DataLabel("TripBcyte", random_bag()))

    # 2 duplicates
    for _ in range(2):
        labels.append(DataLabel("DualAcyte", random_bag()))
    for _ in range(2):
        labels.append(DataLabel("DualBcyte", random_bag()))

    # 5 singles
    solo_names = ["SoloAcyte", "SoloBcyte", "SoloCcyte", "SoloDcyte", "SoloEcyte"]
    for nm in solo_names:
        labels.append(DataLabel(nm, random_bag()))

    return DataLabelCollection(labels)


def trial2():
    random.seed(42)  # deterministic for testing
    dlc = build_test_collection()
    idoca = ImageAnnotationDocument(name="uggy smeal", width=900, height=800, data=dlc)

    print("ORIGINAL DOC:")
    print(idoca)
    print()

    # JSON round-trip
    dlc_json = idoca.to_json()
    dlc2 = ImageAnnotationDocument.from_json(dlc_json)

    print("RECONSTRUCTED DOC (from JSON):")
    print(dlc2)
