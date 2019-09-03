from typing import Optional, List, Sequence, TYPE_CHECKING
if TYPE_CHECKING:
    from projectreport.analyzer.project import Project
from cached_property import cached_property
import git


class Analyzable:

    def __init__(self, path: str, project: Optional['Project'] = None):
        self.path = path
        self.project = project




