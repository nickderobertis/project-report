import abc
from pathlib import Path

from cached_property import cached_property

from projectreport.analyzer.parsers.base import Parser
from projectreport.analyzer.parsers.data_types import ParserDataType


class SingleFileParser(Parser, abc.ABC):
    data_type = ParserDataType.SINGLE_FILE

    @cached_property
    def contents(self) -> str:
        with open(self.path, encoding="utf8") as f:
            file_contents = f.read()
        return file_contents

    @cached_property
    def file_name(self) -> str:
        return Path(self.path).with_suffix("").name

    @classmethod
    def matches_path(cls, path: str) -> bool:
        raise NotImplementedError
