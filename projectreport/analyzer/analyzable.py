from typing import Optional, Dict, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from projectreport.analyzer.project import Project
from cached_property import cached_property
import git


class Analyzable:
    parser = None
    analysis = None

    def __init__(self, path: str, project: Optional['Project'] = None):
        self.path = path
        self.project = project

    @cached_property
    def docstring(self) -> Optional[str]:
        if self.parser is None:
            return None
        return self.parser.docstring

    @cached_property
    def data(self) -> Dict[str, Union[str, int, dict]]:
        data = {}
        data.update(self.analysis.data)
        data.update(dict(
            docstring=self.docstring,
        ))
        return data




