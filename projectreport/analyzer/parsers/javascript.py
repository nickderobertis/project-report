import json
import warnings
from typing import Any, Dict, Optional

from cached_property import cached_property

from projectreport.analyzer.parsers.base import Parser
from projectreport.version import Version


class PackageJSONParser(Parser):
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
        return Version.from_str(self.parsed.get("version"))
