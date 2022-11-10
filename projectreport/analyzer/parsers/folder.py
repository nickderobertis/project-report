import abc
from pathlib import Path
from typing import Optional, Sequence

from cached_property import cached_property

from projectreport.analyzer.parsers.base import Parser
from projectreport.analyzer.parsers.data_types import ParserDataType
from projectreport.license.finder import find_license_file
from projectreport.license.model import License
from projectreport.license.parsing import license_text_to_license


class FolderParser(Parser, abc.ABC):
    """
    :param path: This should be the path of a folder, rather than a path to a file
      that the singular parsers accept.
    :param file_names: A list of file names that should be analyzed within the folder.
    """

    data_type = ParserDataType.FOLDER

    def __init__(
        self,
        path: str,
        file_names: Sequence[str],
    ):
        self.file_names = file_names
        super().__init__(path)

    @classmethod
    def matches_path(cls, path: str, file_names: Sequence[str]) -> bool:
        return find_license_file(Path(path)) is not None

    @cached_property
    def license(self) -> Optional[License]:
        license_file = find_license_file(Path(self.path))
        if license_file is None:
            return None
        license_text = license_file.read_text()
        return license_text_to_license(license_text)
