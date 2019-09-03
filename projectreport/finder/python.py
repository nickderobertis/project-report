from projectreport.finder.base import Finder


class PythonPackageFinder(Finder):

    def __init__(self, recursive: bool = True):
        super().__init__(recursive=recursive, required_files=('__init__.py',))

