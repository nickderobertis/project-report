from typing import List, Optional
import os
import pygount


class PythonModule:

    def __init__(self, path: str, package: Optional[str] = None):
        self.path = path
        self.name = os.path.basename(path).rstrip('.py')
        if package is None:
            package = self.name
        self.package = package
        self.source_analysis = pygount.source_analysis(self.path, self.package)
