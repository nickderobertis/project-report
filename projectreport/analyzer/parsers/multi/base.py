import abc

from cached_property import cached_property

from projectreport.analyzer.parsers.base import Parser


class MultiParser(abc.ABC, Parser):
    """
    :param path: This should be the path of a folder, rather than a path to a file
      that the singular parsers accept.
    """

    @cached_property
    def has_any_match(self) -> bool:
        raise NotImplementedError
