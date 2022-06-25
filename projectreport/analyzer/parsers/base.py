import abc
from typing import ClassVar, List, Optional

from cached_property import cached_property

from projectreport.analyzer.parsers.data_types import ParserDataType


class Parser(abc.ABC):
    data_type: ClassVar[ParserDataType]

    def __init__(self, path: str):
        self.path = path

    @cached_property
    def docstring(self) -> Optional[str]:
        raise NotImplementedError

    @cached_property
    def version(self) -> Optional[str]:
        raise NotImplementedError

    @cached_property
    def topics(self) -> Optional[List[str]]:
        raise NotImplementedError
