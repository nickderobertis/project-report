import os
from pathlib import Path
from typing import Optional, Sequence, Union

import git
from cached_property import cached_property

from projectreport.analyzer.folder import Folder
from projectreport.config import DEFAULT_IGNORE_PATHS
from projectreport.license.finder import find_license_file
from projectreport.license.model import License
from projectreport.license.parser import license_text_to_license


class Project(Folder):
    """
    Pass a project path to get analysis about the project.
    """

    def __init__(
        self,
        path: Union[str, Path],
        excluded_types: Optional[Sequence[str]] = None,
        included_types: Optional[Sequence[str]] = None,
        ignore_paths: Optional[Sequence[str]] = DEFAULT_IGNORE_PATHS,
    ):
        super().__init__(
            path,
            project=self,
            excluded_types=excluded_types,
            included_types=included_types,
            ignore_paths=ignore_paths,
        )

    @cached_property
    def repo(self) -> Optional[git.Repo]:
        try:
            return git.Repo(self.path)
        except git.InvalidGitRepositoryError:
            return None

    @cached_property
    def license(self) -> Optional[License]:
        license_file = find_license_file(Path(self.path))
        if license_file is None:
            return None
        license_text = license_file.read_text()
        return license_text_to_license(license_text)
