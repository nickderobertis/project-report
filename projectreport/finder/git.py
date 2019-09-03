from projectreport.finder.base import Finder


class GitFinder(Finder):

    def __init__(self, recursive: bool = True):
        super().__init__(recursive=recursive, required_folders=('.git',))

