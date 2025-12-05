from data_label import DataLabel
from pixel_bag import PixelBag
import json
from data_label_collection import DataLabelCollection
import random

def make_block_bag(x0: int, y0: int, w: int, h: int) -> PixelBag:
    """
    Helper: build a rectangular block of pixels:
        x in [x0, x0 + w)
        y in [y0, y0 + h)
    """
    bag = PixelBag()
    for x in range(x0, x0 + w):
        for y in range(y0, y0 + h):
            bag.add(x, y)
    return bag


def build_test_collection() -> DataLabelCollection:
    labels = []

    # 2 Lymphocyte labels
    bag_lymph_1 = make_block_bag(10, 20, 3, 4)   # 12 pixels
    bag_lymph_2 = make_block_bag(30, 25, 4, 3)   # 12 pixels
    labels.append(DataLabel("Lymphocyte", bag_lymph_1))
    labels.append(DataLabel("Lymphocyte", bag_lymph_2))

    # 2 Zetacyte labels
    bag_zeta_1 = make_block_bag(50, 10, 5, 2)    # 10 pixels
    bag_zeta_2 = make_block_bag(60, 15, 3, 3)    # 9 pixels
    labels.append(DataLabel("Zetacyte", bag_zeta_1))
    labels.append(DataLabel("Zetacyte", bag_zeta_2))

    # 1 Alphacyte
    bag_alpha = make_block_bag(5, 60, 4, 4)      # 16 pixels
    labels.append(DataLabel("Alphacyte", bag_alpha))

    # 1 Yetacyte
    bag_yeta = make_block_bag(80, 40, 2, 5)      # 10 pixels
    labels.append(DataLabel("Yetacyte", bag_yeta))

    return DataLabelCollection(labels)

def trial():
    # Build original collection
    dlc = build_test_collection()

    print("ORIGINAL COLLECTION:")
    print(dlc)
    print()

    # JSON round-trip
    dlc_json = dlc.to_json()
    dlc2 = DataLabelCollection.from_json(dlc_json)

    print("RECONSTRUCTED COLLECTION (from JSON):")
    print(dlc2)