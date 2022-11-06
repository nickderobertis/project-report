from pathlib import Path
from typing import Optional


def find_license_file(folder: Path) -> Optional[Path]:
    """
    Find a license file in a folder.

    :param folder: The folder to search in.
    :return: The path to the license file, or None if no license file was found.
    """
    for path in folder.glob("*"):
        if path.is_file():
            base_name = path.with_suffix("").name.casefold()
            if base_name in ("license", "copying"):
                return path
    return None
