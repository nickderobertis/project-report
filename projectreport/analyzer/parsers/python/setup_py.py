import ast
from pathlib import Path
from typing import Optional

from cached_property import cached_property

from projectreport.analyzer.parsers.python.base import PythonParser
from projectreport.version import Version


class PythonSetupPyParser(PythonParser):
    @cached_property
    def docstring(self) -> Optional[str]:
        if self.parsed is None:
            return None

        # Walk ast to look for a description kwarg being passed to the setup function.
        # Extract any string that is passed to it
        for node in ast.walk(self.parsed):
            if isinstance(node, ast.keyword) and node.arg == "description":
                if isinstance(node.value, ast.Str):
                    return node.value.s
                elif isinstance(node.value, ast.NameConstant):
                    return node.value.value
        return None

    @cached_property
    def version(self) -> Optional[Version]:
        if self.parsed is None:
            return None
        # Walk ast to look for a version kwarg being passed to the setup function.
        # Extract any string or number that is passed to it
        for node in ast.walk(self.parsed):
            if isinstance(node, ast.keyword) and node.arg == "version":
                if isinstance(node.value, ast.Str):
                    return Version.from_str(node.value.s)
                elif isinstance(node.value, ast.Num):
                    return Version.from_str(str(node.value.n))
        return None

    @classmethod
    def matches_path(cls, path: str) -> bool:
        return Path(path).name == "setup.py"
