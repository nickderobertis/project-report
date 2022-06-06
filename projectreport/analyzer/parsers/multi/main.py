from typing import Final, List, Optional, Sequence, Type

from cached_property import cached_property
from typing_extensions import TypeGuard

from projectreport.analyzer.parsers.base import Parser
from projectreport.analyzer.parsers.data_types import ParserDataType
from projectreport.analyzer.parsers.folder import FolderParser
from projectreport.analyzer.parsers.github import GithubParser
from projectreport.analyzer.parsers.multi.file import MultiFileParser
from projectreport.analyzer.parsers.url import URLParser
from projectreport.logger import logger
from projectreport.parser_types import StandaloneParser
from projectreport.version import Version

# TODO: Improve user ability to customize parsers. Currently they need to mutate the PARSERS
# array and PARSER_DOC_FILES dict to customize parsers as the matches_path classmethod does
# not take into account custom parsers passed by constructor.
PARSERS: Final[List[Type[StandaloneParser]]] = [
    MultiFileParser,
    GithubParser,
]


class MainMultiParser(Parser):
    """
    The main parser that uses other parsers, both single- and multi- together to
    determine information about a folder.
    """

    def __init__(
        self,
        path: str,
        file_names: Sequence[str],
        urls: Optional[Sequence[str]] = None,
        parsers: Optional[List[Type[StandaloneParser]]] = None,
    ):
        """
        :param path: This should be the path of a folder, rather than a path to a file
          that the singular parsers accept.
        :param parsers: Defaults to PARSERS.
        """
        self.parsers = parsers or PARSERS
        self.file_names = file_names
        self.urls = urls or []
        super().__init__(path)

    @classmethod
    def matches_path(
        cls, path: str, file_names: Sequence[str], urls: Optional[Sequence[str]] = None
    ) -> bool:
        urls = urls or []
        for parser in PARSERS:
            if _parser_matches_path(parser, path, file_names, urls):
                return True
        return False

    @cached_property
    def docstring(self) -> Optional[str]:
        return self._get_attr_from_first_parser_to_return_non_none("docstring")

    @cached_property
    def version(self) -> Optional[Version]:
        return self._get_attr_from_first_parser_to_return_non_none("version")

    def _get_attr_from_first_parser_to_return_non_none(self, attr: str):
        for parser in self.parsers:
            if _parser_matches_path(parser, self.path, self.file_names, self.urls):
                parser_obj = _construct_parser(
                    parser, self.path, self.file_names, self.urls
                )
                if parser_obj is None:
                    continue
                value = getattr(parser_obj, attr)
                if value is not None:
                    return value
        return None


def _parser_matches_path(
    parser: Type[StandaloneParser],
    folder: str,
    file_names: Sequence[str],
    urls: Sequence[str],
) -> bool:
    if _is_folder_parser(parser):
        return parser.matches_path(folder, file_names)
    elif _is_url_parser(parser):
        return any([parser.matches_path(url) for url in urls])
    raise NotImplementedError(
        f"No handling for {parser} with data type {parser.data_type}"
    )


def _construct_parser(
    parser: Type[StandaloneParser],
    folder: str,
    file_names: Sequence[str],
    urls: Sequence[str],
) -> Optional[StandaloneParser]:
    if _is_folder_parser(parser):
        return parser(folder, file_names)
    elif _is_url_parser(parser):
        for url in urls:
            if parser.matches_path(url):
                return parser(url)
        logger.warn(f"The URL parser {parser} did not match the given urls {urls}")
        return None
    raise NotImplementedError(
        f"No handling for {parser} with data type {parser.data_type}"
    )


def _is_folder_parser(parser: Type[StandaloneParser]) -> TypeGuard[Type[FolderParser]]:
    return parser.data_type == ParserDataType.FOLDER


def _is_url_parser(parser: Type[StandaloneParser]) -> TypeGuard[Type[URLParser]]:
    return parser.data_type == ParserDataType.URL
