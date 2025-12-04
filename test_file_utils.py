# test_file_utils.py
from __future__ import annotations

import io
from pathlib import Path

import pytest
from PIL import Image

from file_utils import FileUtils


# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "output"


def _make_solid_image(color=(255, 0, 0), size=(16, 16)) -> Image.Image:
    return Image.new("RGB", size, color=color)


# ----------------------------------------------------------------------
# local() and local_text() path construction tests
# ----------------------------------------------------------------------


def test_local_with_subdirectory_no_slashes_explicit_extension():
    """
    subdirectory: yes
    leading/trailing slashes: no
    extension: provided separately
    """
    path = FileUtils.local(
        subdirectory="output/subdirectory_yes/slashes_no",
        name="image_a",
        extension="png",
    )
    expected = ROOT / "output/subdirectory_yes/slashes_no/image_a.png"
    assert path == expected.resolve()


def test_local_with_subdirectory_with_slashes_name_has_extension():
    """
    subdirectory: yes (with outer slashes)
    name: has extension
    extension: None
    """
    path = FileUtils.local(
        subdirectory="/output/subdirectory_yes/slashes_yes/",
        name="/image_b.png",
        extension=None,
    )
    expected = ROOT / "output/subdirectory_yes/slashes_yes/image_b.png"
    assert path == expected.resolve()


def test_local_without_subdirectory_name_contains_path_and_extension():
    """
    subdirectory: None
    name: includes subpath and extension
    extension: None
    """
    path = FileUtils.local(
        subdirectory=None,
        name="output/subdirectory_no/image_c.png",
        extension=None,
    )
    expected = ROOT / "output/subdirectory_no/image_c.png"
    assert path == expected.resolve()


def test_local_with_extension_overriding_name_extension():
    """
    extension parameter overrides any extension in 'name'.
    """
    path = FileUtils.local(
        subdirectory="output/subdirectory_yes/slashes_no",
        name="image_d.jpg",
        extension="png",
    )
    expected = ROOT / "output/subdirectory_yes/slashes_no/image_d.png"
    assert path == expected.resolve()


def test_local_raises_on_empty_name():
    with pytest.raises(ValueError):
        FileUtils.local(subdirectory="anything", name="", extension="txt")


def test_local_text_delegates_to_local():
    """
    local_text should behave like local, just a semantic wrapper.
    """
    path = FileUtils.local_text(
        subdirectory="output/subdirectory_yes",
        name="text_utf_8.txt",
        extension=None,
    )
    expected = ROOT / "output/subdirectory_yes/text_utf_8.txt"
    assert path == expected.resolve()


# ----------------------------------------------------------------------
# Image save/load tests
# ----------------------------------------------------------------------


def test_save_and_load_local_image_with_subdirectory_and_clean_slashes():
    # Use slashes_no case
    img = _make_solid_image(color=(0, 255, 0))
    saved_path = FileUtils.save_local_image(
        img,
        subdirectory="output/subdirectory_yes/slashes_no",
        name="image_a",
        extension="png",
    )
    assert saved_path.is_file()

    loaded = FileUtils.load_local_image(
        subdirectory="output/subdirectory_yes/slashes_no",
        name="image_a",
        extension="png",
    )

    assert loaded.size == img.size
    assert loaded.mode == img.mode


def test_save_and_load_local_image_with_slashes_and_name_extension():
    img = _make_solid_image(color=(0, 0, 255))
    saved_path = FileUtils.save_local_image(
        img,
        subdirectory="/output/subdirectory_yes/slashes_yes/",
        name="/image_b.png",
        extension=None,
    )
    assert saved_path.is_file()

    loaded = FileUtils.load_local_image(
        subdirectory="/output/subdirectory_yes/slashes_yes/",
        name="/image_b.png",
        extension=None,
    )

    assert loaded.size == img.size
    assert loaded.mode == img.mode


def test_save_and_load_image_without_subdirectory_name_has_path():
    img = _make_solid_image(color=(255, 255, 0))
    saved_path = FileUtils.save_local_image(
        img,
        subdirectory=None,
        name="output/subdirectory_no/image_c.png",
        extension=None,
    )
    assert saved_path.is_file()

    loaded = FileUtils.load_local_image(
        subdirectory=None,
        name="output/subdirectory_no/image_c.png",
        extension=None,
    )

    assert loaded.size == img.size
    assert loaded.mode == img.mode


def test_save_and_load_image_direct_path():
    img = _make_solid_image(color=(255, 0, 255))
    direct_path = ROOT / "output/image_d_direct.png"

    FileUtils.save_image(img, direct_path)
    assert direct_path.is_file()

    loaded = FileUtils.load_image(direct_path)
    assert loaded.size == img.size
    assert loaded.mode == img.mode


def test_load_image_missing_raises():
    missing_path = ROOT / "output/this_does_not_exist.png"
    with pytest.raises(FileNotFoundError):
        FileUtils.load_image(missing_path)


# ----------------------------------------------------------------------
# Text save/load tests (UTF-8 and UTF-16, with/without subdirectories)
# ----------------------------------------------------------------------


def test_save_and_load_local_text_utf8_with_subdirectory_no_slashes():
    text = "Hello UTF-8 👋"

    path = FileUtils.save_local_text(
        text,
        subdirectory="output/subdirectory_yes/slashes_no",
        name="text_utf_8",
        extension="txt",
        encoding="utf-8",
    )
    assert path.is_file()

    loaded = FileUtils.load_local_text(
        subdirectory="output/subdirectory_yes/slashes_no",
        name="text_utf_8",
        extension="txt",
        encoding="utf-8",
    )
    assert loaded == text


def test_save_and_load_local_text_utf16_with_subdirectory_and_slashes():
    text = "Hello UTF-16 🌈"

    path = FileUtils.save_local_text(
        text,
        subdirectory="/output/subdirectory_yes/slashes_yes/",
        name="/text_utf_16.txt",
        extension=None,
        encoding="utf-16",
    )
    assert path.is_file()

    loaded = FileUtils.load_local_text(
        subdirectory="/output/subdirectory_yes/slashes_yes/",
        name="/text_utf_16.txt",
        extension=None,
        encoding="utf-16",
    )
    assert loaded == text


def test_save_and_load_text_without_subdirectory_name_has_path_and_extension():
    text = "No subdirectory, explicit path/extension"

    path = FileUtils.save_local_text(
        text,
        subdirectory=None,
        name="output/subdirectory_no/text_utf_8.txt",
        extension=None,
        encoding="utf-8",
    )
    assert path.is_file()

    loaded = FileUtils.load_local_text(
        subdirectory=None,
        name="output/subdirectory_no/text_utf_8.txt",
        extension=None,
        encoding="utf-8",
    )
    assert loaded == text


def test_save_and_load_text_direct_path_utf8():
    text = "Direct path text file"

    direct_path = ROOT / "output/text_direct_utf8.log"
    FileUtils.save_text(text, direct_path, encoding="utf-8")
    assert direct_path.is_file()

    loaded = FileUtils.load_text(direct_path, encoding="utf-8")
    assert loaded == text


def test_load_text_missing_raises():
    missing_path = ROOT / "output/missing.txt"
    with pytest.raises(FileNotFoundError):
        FileUtils.load_text(missing_path, encoding="utf-8")
