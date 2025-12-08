# runner.py
from __future__ import annotations

import random
from typing import List

from runner_params import RunnerParams
from image.bitmap import Bitmap
from background_factory import BackgroundFactory
from circle_factory import CircleFactory
from filesystem.file_utils import FileUtils
from image_utility import ImageUtility
from image.rgba import RGBA
from color_enum import ColorName
from labels.data_label import DataLabel
from circle_label_placement import CircleLabelPlacement
from labels.data_label_collection import DataLabelCollection
from labels.image_annotation_document import ImageAnnotationDocument
import json

class Runner:
    @classmethod
    def run_test(cls, params: RunnerParams) -> None:
        print("Runner.run_test() called")
        cls._debug_print_params(params)

        name = f"{params.file_name_base}_{params.testing_postfix}"
        cls.run(params, name=name, folder="testing", num_colors=3)

    @classmethod
    def run_train(cls, params: RunnerParams) -> None:
        print("Runner.run_train() called")
        cls._debug_print_params(params)

        name = f"{params.file_name_base}_{params.training_postfix}"
        cls.run(params, name=name, folder="training", num_colors=3)

    @classmethod
    def run(
        cls,
        params: RunnerParams,
        name: str,
        folder: str,
        num_colors: int,
    ) -> None:
        print(f"Main Gen Loop @{name} [{folder}]")

        width = params.output_width
        height = params.output_height
        start = params.start_index
        end = params.end_index

        for index in range(start, end + 1):
            number_string_original = str(index)
            zeros_needed = max(params.leading_zeros - len(number_string_original), 0)
            number_string = ("0" * zeros_needed) + number_string_original

            image = cls.make_image(params, width=width, height=height)

            placements: List[CircleLabelPlacement] = []

            placement_attempt_number = 0
            placement_target_count = random.randint(params.target_min, params.target_max)

            while placement_attempt_number < params.max_tries:

                label_id = ColorName.random(num_colors)
                label_name = label_id.label()
                label_rgba = label_id.rgba()

                circle_image = CircleFactory.random()
                
                

                radius = circle_image.width / 2.0
                min_x = (radius / 2.0)
                max_x = image.width - (radius / 2.0)
                min_y = (radius / 2.0)
                max_y = image.height - (radius / 2.0)

                placement_x = random.randint(int(round(min_x)), int(round(max_x)))
                placement_y = random.randint(int(round(min_y)), int(round(max_y)))

                num_intersections = 0
                for placement in placements:
                    if placement.intersects(placement_x, placement_y, radius):
                        num_intersections += 1

                if num_intersections <= params.max_overlap:
                    ImageUtility.recolor_white(circle_image, label_rgba, color_noise=params.color_noise)
                    base_alpha = random.uniform(params.alpha_min, params.alpha_max)
                    ImageUtility.multiply_alpha(circle_image, base_alpha, params.alpha_noise)
                    x = int(round(placement_x - radius))
                    y = int(round(placement_y - radius))
                    image.stamp_alpha(circle_image, x, y)
                    data_label = cls.make_label(params, label_name, circle_image, x, y, 0.2)
                    placement = CircleLabelPlacement(data_label, placement_x, placement_y, radius)
                    placements.append(placement)

                placement_attempt_number += 1
                if len(placements) >= placement_target_count:
                    break
                
            file_name_base = f"{name}_{number_string}"

            image_file_name = file_name_base
            annotation_file_name = f"{file_name_base}_annotations"


            data_labels = [placement.data_label for placement in placements]

            data_label_collection = DataLabelCollection(data_labels)

            image_annotation_document = ImageAnnotationDocument(file_name_base, image.width, image.height, data_label_collection)

            anno_string = json.dumps(image_annotation_document.to_json(), indent=2)

            FileUtils.save_local_text(
                anno_string,
                folder,
                annotation_file_name,
                "json",
            )
            FileUtils.save_local_image(
                image.export_pillow(),
                folder,
                image_file_name,
                "png",
            )

    @classmethod
    def make_label(
        cls,
        params: RunnerParams,
        label_name: str,
        glyph: Bitmap,
        x: int,
        y: int,
        alpha_threshold: float
    ) -> DataLabel:
        """
        Build a DataLabel by scanning the glyph bitmap and collecting
        all pixels whose alpha (0–1) exceeds alpha_threshold, translated
        into global coordinates by (x, y).

        Only pixels that fall inside the final image bounds
        [0, width-1] x [0, height-1] are recorded.
        """
        label = DataLabel(name=label_name)

        gw = glyph.width
        gh = glyph.height

        img_w = params.output_width
        img_h = params.output_height

        for gy in range(gh):
            for gx in range(gw):
                px = glyph.rgba[gx][gy]
                if px.af <= alpha_threshold:
                    continue

                world_x = x + gx
                world_y = y + gy

                # Clip to image bounds; skip OOB pixels entirely
                if 0 <= world_x < img_w and 0 <= world_y < img_h:
                    label.add(world_x, world_y)

        return label




    @classmethod
    def make_image(
        cls,
        params: RunnerParams,
        width: int = 256,
        height: int = 256,
    ) -> Bitmap:
        background = BackgroundFactory.random()

        result = Bitmap()
        result.allocate(width=width, height=height)

        span_x = background.width - width
        span_y = background.height - height

        offset_x = 0
        if span_x > 0:
            offset_x = -random.randint(0, span_x)

        offset_y = 0
        if span_y > 0:
            offset_y = -random.randint(0, span_y)

        result.stamp(background, offset_x, offset_y)

        return result

    @classmethod
    def _debug_print_params(cls, params: RunnerParams) -> None:
        print("Runner params snapshot:")
        for field_name, value in vars(params).items():
            print(f"  {field_name}: {value}")
