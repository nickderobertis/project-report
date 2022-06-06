import abc
from pathlib import Path

from cached_property import cached_property

from projectreport.analyzer.parsers.base import Parser


class FileParser(abc.ABC, Parser):
    @cached_property
    def contents(self) -> str:
        with open(self.path, encoding="utf8") as f:
            file_contents = f.read()
        return file_contents

    @cached_property
    def file_name(self) -> str:
        return Path(self.path).with_suffix("").name
