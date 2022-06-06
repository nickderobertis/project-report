import os
from typing import Dict, Optional, Sequence

from cached_property import cached_property

from projectreport.analyzer.parsers.base import Parser
from projectreport.analyzer.parsers.folder import FolderParser
from projectreport.analyzer.parsers.index import PARSER_DOC_FILES
from projectreport.version import Version


class MultiFileParser(FolderParser):
    def __init__(
        self,
        path: str,
        file_names: Sequence[str],
        file_parsers: Optional[Dict[str, Parser]] = None,
    ):
        """
        :param path: This should be the path of a folder, rather than a path to a file
          that the other parsers accept.
        :param file_parsers: Defaults to PARSER_DOC_FILES.
        """
        self.file_parsers = file_parsers or PARSER_DOC_FILES
        super().__init__(path, file_names)

    @cached_property
    def docstring(self) -> Optional[str]:
        return self._get_attr_from_first_parser_to_return_non_none("docstring")

    @cached_property
    def version(self) -> Optional[Version]:
        return self._get_attr_from_first_parser_to_return_non_none("version")

    @classmethod
    def matches_path(cls, path: str, file_names: Sequence[str]) -> bool:
        for file, parser in PARSER_DOC_FILES.items():
            if file in file_names:
                return True
        return False

    def _get_attr_from_first_parser_to_return_non_none(self, attr: str):
        for file, parser in self.file_parsers.items():
            if file in self.file_names:
                full_path = os.path.join(self.path, file)
                parser = PARSER_DOC_FILES[file](full_path)
                value = getattr(parser, attr)
                if value is not None:
                    return value
        return None
