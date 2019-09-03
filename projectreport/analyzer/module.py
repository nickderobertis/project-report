from typing import List, Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from projectreport.analyzer.project import Project
    from projectreport.analyzer.parsers.base import Parser
import os
from cached_property import cached_property

from projectreport.analyzer.analyzable import Analyzable
from projectreport.analyzer.analysis import ModuleAnalysis
from projectreport.analyzer.parsers.index import PARSER_EXTENSIONS


class Module(Analyzable):

    def __init__(self, path: str, package: Optional[str] = None, project: Optional['Project'] = None):
        base_path, extension = os.path.splitext(path)
        self.name = os.path.basename(base_path)
        self.extension = extension.strip('.')
        if package is None:
            package = self.name
        self.package = package
        super().__init__(path, project=project)
        self.analysis = ModuleAnalysis(self)

    @cached_property
    def parser(self) -> Optional['Parser']:
        if self.extension not in PARSER_EXTENSIONS:
            return None
        return PARSER_EXTENSIONS[self.extension](self.path)

