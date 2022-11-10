from typing import TYPE_CHECKING, Dict, List, Optional, Union

from projectreport.data import AnalysisData
from projectreport.license.model import License
from projectreport.logger import logger
from projectreport.version import Version

if TYPE_CHECKING:
    from projectreport.analyzer.project import Project
    from projectreport.analyzer.analysis import Analysis
    from projectreport.analyzer.parsers.base import Parser

from cached_property import cached_property


class Analyzable:
    parser: Optional["Parser"] = None
    analysis: Optional["Analysis"] = None
    name: Optional[str] = None

    def __init__(self, path: str, project: Optional["Project"] = None):
        self.path = path
        self.project = project

    @cached_property
    def docstring(self) -> Optional[str]:
        if self.parser is None:
            return None
        return self.parser.docstring

    @cached_property
    def version(self) -> Optional[Version]:
        if self.parser is None:
            return None
        return self.parser.version

    @cached_property
    def topics(self) -> Optional[List[str]]:
        if self.parser is None:
            return None
        return self.parser.topics

    @cached_property
    def license(self) -> Optional[License]:
        if self.parser is None:
            return None
        return self.parser.license

    @cached_property
    def data(self) -> AnalysisData:
        if self.analysis is None:
            raise ValueError(
                "cannot get data from Analyzable if no analysis is attached"
            )
        logger.debug(f"Getting data for {self.path}")

        data: AnalysisData = {}
        data.update(self.analysis.data)
        data.update(
            dict(
                docstring=self.docstring,
                version=str(self.version) if self.version is not None else None,
                topics=self.topics,
                license=self.license.type.value if self.license is not None else None,
            )
        )
        if self.name is not None:
            data.update(dict(name=self.name))
        return data
