import json
import warnings
from pathlib import Path
from typing import Any, Dict, List, Optional

from cached_property import cached_property

from projectreport.analyzer.parsers.file import SingleFileParser
from projectreport.version import Version


class PackageJSONParser(SingleFileParser):
    @cached_property
    def parsed(self) -> Optional[Dict[str, Any]]:
        try:
            return json.loads(self.contents)
        except SyntaxError:
            warnings.warn(f"Could not parse {self.path} due to SyntaxError")
            return None

    @cached_property
    def docstring(self) -> Optional[str]:
        if self.parsed is None:
            return None
        return self.parsed.get("description")

    @cached_property
    def version(self) -> Optional[Version]:
        if self.parsed is None:
            return None
        version_str = self.parsed.get("version")
        if version_str is None:
            return None
        return Version.from_str(version_str)

    @cached_property
    def topics(self) -> Optional[List[str]]:
        if self.parsed is None:
            return None
        return self.parsed.get("keywords")

    @classmethod
    def matches_path(cls, path: str) -> bool:
        return Path(path).name == "package.json"
