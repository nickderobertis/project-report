from typing import Optional, Dict, Any
import warnings
import json
from cached_property import cached_property
from projectreport.analyzer.parsers.base import Parser


class PackageJSONParser(Parser):

    @cached_property
    def parsed(self) -> Optional[Dict[str, Any]]:
        try:
            return json.loads(self.contents)
        except SyntaxError:
            warnings.warn(f'Could not parse {self.path} due to SyntaxError')
            return None

    @cached_property
    def docstring(self) -> Optional[str]:
        if self.parsed is None:
            return None
        return self.parsed.get("description")
