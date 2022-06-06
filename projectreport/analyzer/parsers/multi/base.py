import abc
from typing import Optional

from cached_property import cached_property

from projectreport.version import Version


class MultiParser(abc.ABC):
    def __init__(
        self,
        path: str,
    ):
        """
        :param path: This should be the path of a folder, rather than a path to a file
          that the singular parsers accept.
        """
        self.path = path

    @cached_property
    def has_any_match(self) -> bool:
        raise NotImplementedError

    @cached_property
    def docstring(self) -> Optional[str]:
        raise NotImplementedError

    @cached_property
    def version(self) -> Optional[Version]:
        raise NotImplementedError
