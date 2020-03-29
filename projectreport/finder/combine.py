from typing import Sequence
import os
from projectreport.finder.base import Finder


class CombinedFinder(Finder):
    """
    Finder which can be passed other specific finders, and will return project paths that match any of the
    passed finders.
    """

    def __init__(self, finders: Sequence[Finder], recursive: bool = True):
        self.finders = finders
        super().__init__(recursive=recursive)
        self.file_extensions = []
        for finder in self.finders:
            if finder.file_extensions:
                self.file_extensions.extend(finder.file_extensions)

    def is_valid(self, path: str):
        is_valid = False
        for finder in self.finders:
            if finder.is_valid(path):
                is_valid = True
        return is_valid
