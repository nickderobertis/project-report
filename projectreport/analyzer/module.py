from typing import List, Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from projectreport.analyzer.project import Project
import os
import pygount

from projectreport.analyzer.analyzable import Analyzable
from projectreport.analyzer.analysis import ModuleAnalysis


class Module(Analyzable):

    def __init__(self, path: str, package: Optional[str] = None, project: Optional['Project'] = None):
        self.name = os.path.basename(path).rstrip('.py')
        if package is None:
            package = self.name
        self.package = package
        super().__init__(path, project=project)
        self.analysis = ModuleAnalysis(self)

