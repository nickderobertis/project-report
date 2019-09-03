from typing import Optional, List, Sequence, TYPE_CHECKING
if TYPE_CHECKING:
    from projectreport.analyzer.module import Module
    from projectreport.analyzer.analyzable import Analyzable
    from projectreport.analyzer.folder import Folder
from copy import deepcopy
from datetime import datetime
import pygount
from cached_property import cached_property
import git


class FolderAnalysis:

    def __init__(self, folder: 'Folder'):
        self.lines = {key: 0 for key in [
            'code',
            'documentation',
            'empty',
            'string'
        ]}
        self.git_analysis = GitAnalysis(folder)

    def __repr__(self):
        return f'<PackageAnalysis(lines={self.lines})>'

    def add_module_analysis(self, analysis: 'ModuleAnalysis'):
        for attr in self.lines:
            value = getattr(analysis.source_analysis, attr)
            if value is None:
                value = 0
            self.lines[attr] += value

    def add_subfolder_analysis(self, analysis: 'FolderAnalysis'):
        for attr in self.lines:
            value = analysis.lines[attr]
            if value is None:
                value = 0
            self.lines[attr] += value


class ModuleAnalysis:

    def __init__(self, module: 'Module'):
        self.module = module
        self.source_analysis = pygount.source_analysis(self.module.path, self.module.package)
        self.git_analysis = GitAnalysis(self.module)


class GitAnalysis:

    def __init__(self, analyzable: 'Analyzable'):
        self.ref = analyzable

    @cached_property
    def commits(self) -> Optional[List[git.Commit]]:
        if not self.has_repo:
            return None
        commits = [commit for commit in self.ref.project.repo.iter_commits(paths=self.ref.path)]
        return commits

    # @cached_property
    # def first_commit(self) -> Optional[git.Commit]:
    #     """
    #     For some reason, errors are coming in trying to access properties of the first commits.
    #     This gets the first working commit.
    #     :return:
    #     """
    #     if not self.has_repo:
    #         return None
    #     commits = deepcopy(self.commits)
    #     commits.reverse()
    #     for commit in commits:
    #         try:
    #             commit.summary
    #         except ValueError as e:
    #             if 'SHA could not be resolved' in e:
    #                 # For some reason this commit doesn't work, try the next one
    #                 continue
    #             else:
    #                 raise e
    #         # This is a valid commit, return it
    #         return commit



    @cached_property
    def num_commits(self) -> Optional[int]:
        if not self.has_repo:
            return None
        return len(self.commits)

    @cached_property
    def created(self) -> Optional[datetime]:
        return self.commits[-1].committed_datetime

    @cached_property
    def updated(self) -> Optional[datetime]:
        return self.commits[0].committed_datetime

    @cached_property
    def has_repo(self) -> bool:
        return self.ref.project is not None and self.ref.project.repo is not None

