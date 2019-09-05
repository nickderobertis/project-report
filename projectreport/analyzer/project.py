from typing import Optional, Sequence
import os
from cached_property import cached_property
import git

from projectreport.analyzer.folder import Folder
from projectreport.config import DEFAULT_IGNORE_PATHS


class Project(Folder):
    """
    Pass a project path to get analysis about the project.
    """

    def __init__(self, path: str, excluded_types: Optional[Sequence[str]] = None,
                 included_types: Optional[Sequence[str]] = None,
                 ignore_paths: Optional[Sequence[str]] = DEFAULT_IGNORE_PATHS):
        super().__init__(
            path,
            project=self,
            excluded_types=excluded_types,
            included_types=included_types,
            ignore_paths=ignore_paths
        )

    @cached_property
    def repo(self) -> Optional[git.Repo]:
        try:
            return git.Repo(self.path)
        except git.InvalidGitRepositoryError:
            return None


