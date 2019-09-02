from typing import Optional, List, Sequence, TYPE_CHECKING
if TYPE_CHECKING:
    from projectreport.analyzer.project import Project
from cached_property import cached_property
import git


class Analyzable:

    def __init__(self, path: str, project: Optional['Project'] = None):
        self.path = path
        self.project = project

    @cached_property
    def commits(self) -> Optional[List[git.Commit]]:
        if not self.has_repo:
            return None
        return [commit for commit in self.project.repo.iter_commits(paths=self.path)]

    @cached_property
    def num_commits(self) -> Optional[int]:
        if not self.has_repo:
            return None
        return len(self.commits)

    @cached_property
    def has_repo(self) -> bool:
        return self.project is not None and self.project.repo is not None




