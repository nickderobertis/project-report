from typing import Optional, Sequence
import os
from cached_property import cached_property
import git

from projectreport.analyzer.folder import Folder


class Project(Folder):

    def __init__(self, path: str, excluded_types: Optional[Sequence[str]] = None,
                 included_types: Optional[Sequence[str]] = None):
        super().__init__(path, project=self, excluded_types=excluded_types, included_types=included_types)

    @cached_property
    def repo(self) -> Optional[git.Repo]:
        try:
            return git.Repo(self.path)
        except git.InvalidGitRepositoryError:
            return None


