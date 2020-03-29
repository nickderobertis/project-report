from typing import Optional, Dict, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from projectreport.analyzer.project import Project
    from projectreport.analyzer.analysis import Analysis
    from projectreport.analyzer.parsers.base import Parser
from cached_property import cached_property


class Analyzable:
    parser: Optional['Parser'] = None
    analysis: Optional['Analysis'] = None
    name: Optional[str] = None

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
        if self.analysis is None:
            raise ValueError('cannot get data from Analyzable if no analysis is attached')

        data: Dict[str, Union[str, int, dict]] = {}
        data.update(self.analysis.data)
        data.update(dict(
            docstring=self.docstring,
        ))
        if self.name is not None:
            data.update(dict(name=self.name))
        return data




