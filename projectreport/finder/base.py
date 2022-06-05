import os
from typing import List, Optional, Sequence

from projectreport.config import DEFAULT_IGNORE_PATHS
from projectreport.tools.expand_glob import all_possible_paths


class Finder:
    """
    Class for finding projects by required folders or files, or looking for certain file extensions.
    """

    def __init__(
        self,
        recursive: bool = True,
        required_folders: Optional[Sequence[str]] = None,
        required_files: Optional[Sequence[str]] = None,
        file_extensions: Optional[Sequence[str]] = None,
    ):
        self.recursive = recursive
        self.required_folders = required_folders
        self.required_files = required_files
        self.file_extensions = file_extensions
        self.project_paths: List[str] = []

    def find(
        self, path: str, ignore_paths: Optional[Sequence[str]] = DEFAULT_IGNORE_PATHS
    ):
        if ignore_paths:
            all_ignore_paths = all_possible_paths(ignore_paths, path)
        else:
            all_ignore_paths = []

        if path in all_ignore_paths:
            # Ignored, do nothing and return
            return self.project_paths

        _, folders, files = next(os.walk(path))

        if self.is_valid(path):
            self.project_paths.append(path)
            if not self.recursive:
                # Stop searching a folder once a project is found
                return self.project_paths

        for folder in folders:
            folder_path = os.path.join(path, folder)
            if folder_path in all_ignore_paths:
                continue
            self.find(folder_path, ignore_paths=ignore_paths)

        return self.project_paths

    def find_all(
        self,
        paths: Sequence[str],
        ignore_paths: Optional[Sequence[str]] = DEFAULT_IGNORE_PATHS,
    ):
        [self.find(path, ignore_paths=ignore_paths) for path in paths]
        return self.project_paths

    def is_valid(self, path: str):
        _, folders, files = next(os.walk(path))
        if self.required_folders:
            for req_folder in self.required_folders:
                if req_folder not in folders:
                    return False
        if self.required_files:
            for req_file in self.required_files:
                if req_file not in files:
                    return False
        if self.file_extensions:
            extensions = {os.path.splitext(file)[1].strip(".") for file in files}
            has_extension = False
            for file_ext in self.file_extensions:
                if file_ext in extensions:
                    has_extension = True
            if not has_extension:
                return False

        return True

    def _validate(self):
        if not any([self.required_folders, self.required_files, self.file_extensions]):
            raise ValueError("must provide some conditions")
