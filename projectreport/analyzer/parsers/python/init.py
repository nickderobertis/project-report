import ast
from pathlib import Path
from typing import Optional

from cached_property import cached_property

from projectreport.analyzer.parsers.python.base import PythonParser
from projectreport.version import Version


class PythonInitParser(PythonParser):
    @cached_property
    def docstring(self) -> Optional[str]:
        if self.parsed is None:
            return None
        return ast.get_docstring(self.parsed)

    @cached_property
    def version(self) -> Optional[Version]:
        if self.parsed is None:
            return None
        # Walk ast to look for __version__ variable. If it is defined, extract the version from it
        for node in ast.walk(self.parsed):
            if isinstance(node, ast.Assign) and node.targets[0].id == "__version__":  # type: ignore
                # Extract version from __version__ = "1.2.3"
                if isinstance(node.value, ast.Str):
                    return Version.from_str(node.value.s)
                # Extract version from __version__ = 1.2
                elif isinstance(node.value, ast.Num):
                    return Version.from_str(str(node.value.n))
        return None

    @classmethod
    def matches_path(cls, path: str) -> bool:
        return Path(path).name == "__init__.py"
