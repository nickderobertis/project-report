from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from projectreport.analyzer.module import Module
    from projectreport.analyzer.analyzable import Analyzable
    from projectreport.analyzer.folder import Folder

from datetime import datetime

import pygount
from cached_property import cached_property
from git import Commit  # type: ignore


class Analysis:
    _loc: Optional[int] = None
    _full_loc: Optional[int] = None

    def __init__(self, analyzable: "Analyzable"):
        self.git_analysis = GitAnalysis(analyzable)

    @cached_property
    def data(self):
        return dict(
            num_commits=self.git_analysis.num_commits,
            created=self.git_analysis.created,
            updated=self.git_analysis.updated,
            lines=self.loc,
            full_lines=self.full_loc,
            urls=self.git_analysis.urls,
        )

    @property
    def loc(self) -> Optional[int]:
        return self._loc

    @loc.setter
    def loc(self, value: int):
        self._loc = value

    @property
    def full_loc(self) -> Optional[int]:
        return self._full_loc

    @full_loc.setter
    def full_loc(self, value: int):
        self._full_loc = value


class FolderAnalysis(Analysis):
    def __init__(self, folder: "Folder"):
        self.lines = {key: 0 for key in ["code", "documentation", "empty", "string"]}
        super().__init__(folder)

    def __repr__(self):
        return f"<FolderAnalysis(lines={self.lines})>"

    def add_module_analysis(self, analysis: "ModuleAnalysis"):
        for attr in self.lines:
            value = getattr(analysis.source_analysis, attr)
            if value is None:
                value = 0
            self.lines[attr] += value

    def add_subfolder_analysis(self, analysis: "FolderAnalysis"):
        for attr in self.lines:
            value = analysis.lines[attr]
            if value is None:
                value = 0
            self.lines[attr] += value

    @property
    def loc(self) -> int:
        return self.lines["code"]

    @loc.setter
    def loc(self, value: int):
        raise NotImplementedError

    @property
    def full_loc(self) -> int:
        loc = 0
        keys = ["code", "documentation", "empty", "string"]
        for key in keys:
            loc += self.lines[key]
        return loc

    @full_loc.setter
    def full_loc(self, value: int):
        raise NotImplementedError


class ModuleAnalysis(Analysis):
    def __init__(self, module: "Module"):
        self.module = module
        self.source_analysis: pygount.SourceAnalysis = pygount.SourceAnalysis.from_file(
            self.module.path, self.module.package
        )
        self.loc = self.source_analysis.code

        full_loc = 0
        for key in ["code", "documentation", "empty", "string"]:
            full_loc += getattr(self.source_analysis, key, 0)
        self.full_loc = full_loc
        super().__init__(module)


class GitAnalysis:
    def __init__(self, analyzable: "Analyzable"):
        self.ref = analyzable

    @cached_property
    def commits(self) -> Optional[List[Commit]]:
        if not self.has_repo:
            return None
        if self.ref.project is None:  # for mypy
            return None
        commits = [
            commit for commit in self.ref.project.repo.iter_commits(paths=self.ref.path)
        ]
        return commits

    @cached_property
    def num_commits(self) -> Optional[int]:
        if not self.has_repo:
            return None
        return len(self.commits)

    @cached_property
    def created(self) -> Optional[datetime]:
        if not self.commits:
            return None
        return self.commits[-1].committed_datetime

    @cached_property
    def updated(self) -> Optional[datetime]:
        if not self.commits:
            return None
        return self.commits[0].committed_datetime

    @cached_property
    def has_repo(self) -> bool:
        return self.ref.project is not None and self.ref.project.repo is not None

    @cached_property
    def has_remote(self) -> bool:
        if self.ref.project is None:
            return False
        try:
            self.ref.project.repo.remote()
            return True
        except ValueError as e:
            if "Remote named 'origin' didn't exist" in str(e):
                # Repo does not have remote
                return False
            else:
                raise e

    @cached_property
    def urls(self) -> Optional[List[str]]:
        if not self.has_repo or not self.has_remote:
            return None
        if self.ref.project is None:  # for mypy
            return None
        urls = list(self.ref.project.repo.remote().urls)

        # Urls currently have .git on the end, strip
        urls = [url[:-4] if url.endswith(".git") else url for url in urls]
        return urls
