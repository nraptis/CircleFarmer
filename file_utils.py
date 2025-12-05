# file_utils.py
from __future__ import annotations

from pathlib import Path
from typing import Union

from PIL import Image


PathLike = Union[str, Path]


class FileUtils:

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    @classmethod
    def _strip_outer_slashes(cls, s: str) -> str:
        """
        Remove leading and trailing slashes only.
        Internal slashes remain untouched.
        """
        if not isinstance(s, str):
            raise TypeError("Path components must be strings")
        return s.lstrip("/\\").rstrip("/\\")

    @classmethod
    def _ensure_parent_dir(cls, path: Path) -> None:
        """
        Ensure the parent directory for a path exists.
        """
        parent = path.parent
        if not parent.exists():
            parent.mkdir(parents=True, exist_ok=True)

    @classmethod
    def _to_path(cls, p: PathLike) -> Path:
        if isinstance(p, Path):
            return p.resolve()
        return Path(p).resolve()

    # ------------------------------------------------------------------
    # Core path builder for generic files
    # ------------------------------------------------------------------
    @classmethod
    def local(
        cls,
        subdirectory: str | None = None,
        name: str | None = None,
        extension: str | None = None,
    ) -> Path:
        if name is None or len(name.strip()) == 0:
            raise ValueError("FileUtils.local requires a non-empty 'name' parameter")

        # Normalize only outer slashes
        if subdirectory:
            subdirectory = cls._strip_outer_slashes(subdirectory)
        name = cls._strip_outer_slashes(name)

        name_path = Path(name)

        # Determine extension, preserving any internal path in "name"
        if extension:
            extension = extension.lstrip(".")
            parent = name_path.parent
            stem = name_path.stem

            if str(parent) == ".":
                # No nested path in name, just use the stem
                file_name = f"{stem}.{extension}"
            else:
                # Preserve the path portion from name
                file_name = str(parent / f"{stem}.{extension}")
        else:
            # assume name already contains its extension if needed
            file_name = name

        project_root = Path(__file__).resolve().parent

        if subdirectory:
            final_path = project_root / subdirectory / file_name
        else:
            final_path = project_root / file_name

        return final_path.resolve()


    # ------------------------------------------------------------------
    # Images
    # ------------------------------------------------------------------

    # 1.) load_local_image
    # 2.) load_image(cls, file_path)
    # 3.) save_local_image
    # 4.) save_image(cls, image, file_path)

    @classmethod
    def load_image(cls, file_path: PathLike) -> Image.Image:
        """
        Load an image from an explicit path.
        """
        path = cls._to_path(file_path)
        
        if not path.is_file():
            raise FileNotFoundError(f"Image file not found: {path}")

        try:
            img = Image.open(path)
            img.load()  # force read into memory
            return img
        except OSError as e:
            raise OSError(f"Failed to load image: {path}") from e

    @classmethod
    def load_local_image(
        cls,
        subdirectory: str | None = None,
        name: str | None = None,
        extension: str | None = None,
    ) -> Image.Image:
        """
        Load an image using local() as the path builder.
        """
        path = cls.local(subdirectory=subdirectory, name=name, extension=extension)
        return cls.load_image(path)

    @classmethod
    def save_image(cls, image: Image.Image, file_path: PathLike) -> Path:
        """
        Save a Pillow Image to a specific path.

        - Creates parent directories if needed.
        - Returns the resolved Path actually written.
        """
        file_path = cls._to_path(file_path)
        cls._ensure_parent_dir(file_path)
        image.save(file_path)
        return file_path

    @classmethod
    def save_local_image(
        cls,
        image: Image.Image,
        subdirectory: str | None = None,
        name: str | None = None,
        extension: str | None = None,
    ) -> Path:
        """
        Build a local path (via FileUtils.local) and save the image there.

        Returns:
            The resolved Path actually written.
        """
        path = cls.local(subdirectory=subdirectory, name=name, extension=extension)
        return cls.save_image(image, path)

    # ------------------------------------------------------------------
    # Text files
    # ------------------------------------------------------------------

    # 1.) load_local_text (returns the file contents as string)
    # 2.) load_text(cls, file_path) (returns the file contents as string)
    # 3.) save_local_text
    # 4.) save_text(cls, file_path)

    @classmethod
    def local_text(
        cls,
        subdirectory: str | None = None,
        name: str | None = None,
        extension: str | None = None,
    ) -> Path:
        """
        Build a local path for a text file.

        Rules:
        - 'name' is required and may include its own path.
        - No default extension behavior.
        - If extension is provided, override any existing one in name.
        - If no extension is provided anywhere, allow extensionless file.
        """
        if name is None or len(name.strip()) == 0:
            raise ValueError("FileUtils.local_text requires a non-empty 'name' parameter")

        # Delegate to local(), which already does the right thing.
        return cls.local(subdirectory=subdirectory, name=name, extension=extension)

    @classmethod
    def load_text(cls, file_path: PathLike, encoding: str) -> str:
        """
        Load text from an explicit path using the given encoding.

        Caller is responsible for providing the correct encoding.

        Returns:
            The file contents as str.

        Raises:
            FileNotFoundError
            UnicodeDecodeError
            OSError for IO-related issues
        """
        path = cls._to_path(file_path)

        if not path.is_file():
            raise FileNotFoundError(f"Text file not found: {path}")

        with path.open("r", encoding=encoding) as f:
            return f.read()

    @classmethod
    def load_local_text(
        cls,
        subdirectory: str | None = None,
        name: str | None = None,
        extension: str | None = None,
        encoding: str = "utf-8",
    ) -> str:
        """
        Build a local path (via local_text) and load its contents
        using the given encoding.
        """
        path = cls.local_text(subdirectory=subdirectory, name=name, extension=extension)
        return cls.load_text(path, encoding=encoding)

    @classmethod
    def save_text(cls, text: str, file_path: PathLike, encoding: str) -> Path:
        """
        Save a text string to a specific path using the given encoding.

        - Creates parent directories if needed.
        - Returns the resolved Path actually written.
        """
        path = cls._to_path(file_path)
        cls._ensure_parent_dir(path)

        with path.open("w", encoding=encoding) as f:
            f.write(text)

        return path

    @classmethod
    def save_local_text(
        cls,
        text: str,
        subdirectory: str | None = None,
        name: str | None = None,
        extension: str | None = None,
        encoding: str = "utf-8",
    ) -> Path:
        """
        Build a local text path (via local_text) and save the string there
        using the given encoding.

        Returns:
            The resolved Path actually written.
        """
        path = cls.local_text(subdirectory=subdirectory, name=name, extension=extension)
        return cls.save_text(text, path, encoding=encoding)