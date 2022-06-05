from projectreport.finder.base import Finder


class JavaScriptPackageFinder(Finder):
    """
    Finder which automatically looks for projects with JavaScript packages.
    """

    def __init__(self, recursive: bool = True):
        super().__init__(recursive=recursive, required_files=("package.json",))
