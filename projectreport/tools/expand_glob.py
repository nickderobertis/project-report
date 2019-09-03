from typing import List, Sequence, Optional
import os
import glob


def all_possible_paths(paths: Sequence[str], base_path: Optional[str] = None) -> List[str]:
    all_paths = []
    for path in paths:
        # If got a relative path and a base path was passed
        if base_path is not None and not os.path.isabs(path):
            full_path = os.path.join(base_path, path)
        else:
            full_path = path
        all_paths.extend(glob.glob(full_path, recursive=False))
    return all_paths
