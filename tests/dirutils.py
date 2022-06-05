import contextlib
import tempfile
from pathlib import Path
from typing import Iterator


@contextlib.contextmanager
def create_temp_path() -> Iterator[Path]:
    """
    Returns a temporary folder path

    Use this instead of tempfile.TemporaryDirectory because:
    1. That returns a string and not a path
    2. On MacOS, the temp directory has a symlink. This resolves the symlink so that
       there won't be any mismatch in resolved paths.
    3. On Windows, the temp directory can fail to delete with a PermissionError. This function
       will try to delete the temp directory, but if it fails with PermissionError or OSError
       it will just ignore it.
    """
    temp_dir = tempfile.TemporaryDirectory()
    temp_path = Path(temp_dir.name).resolve()
    yield temp_path
    try:
        temp_dir.cleanup()
    except (PermissionError, OSError):
        pass
