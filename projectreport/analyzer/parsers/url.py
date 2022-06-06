import abc

from projectreport.analyzer.parsers.base import Parser
from projectreport.analyzer.parsers.data_types import ParserDataType


class URLParser(Parser, abc.ABC):
    data_type = ParserDataType.URL

    @classmethod
    def matches_path(cls, path: str) -> bool:
        raise NotImplementedError
