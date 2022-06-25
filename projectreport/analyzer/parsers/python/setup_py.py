import ast
from pathlib import Path
from typing import List, Optional

from cached_property import cached_property

from projectreport.analyzer.parsers.python.base import PythonParser
from projectreport.analyzer.parsers.python.classifier_topics import (
    get_topics_from_classifiers,
)
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

    @cached_property
    def topics(self) -> Optional[List[str]]:
        if self.parsed is None:
            return None
        # Walk ast to look for a classifiers kwarg being passed to the setup function.
        # Extract any string that is passed to it
        classifiers: Optional[List[str]] = None
        for node in ast.walk(self.parsed):
            if isinstance(node, ast.keyword) and node.arg == "classifiers":
                if isinstance(node.value, ast.List):
                    classifiers = [x.s for x in node.value.elts]  # type: ignore
                elif isinstance(node.value, ast.Str):
                    classifiers = [node.value.s]
        if classifiers is None:
            return None
        return get_topics_from_classifiers(classifiers)

    @classmethod
    def matches_path(cls, path: str) -> bool:
        return Path(path).name == "setup.py"
