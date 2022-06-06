from typing import Union

from projectreport.analyzer.parsers.folder import FolderParser
from projectreport.analyzer.parsers.url import URLParser

StandaloneParser = Union[FolderParser, URLParser]
