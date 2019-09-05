from projectreport.finder.base import Finder


class GitFinder(Finder):
    """
    Finder which automatically looks for projects with git repositories.
    """

    def __init__(self, recursive: bool = True):
        super().__init__(recursive=recursive, required_folders=('.git',))

