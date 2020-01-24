from typing import Optional
import ast
import warnings
from cached_property import cached_property
from projectreport.analyzer.parsers.base import Parser


class PythonParser(Parser):

    @cached_property
    def parsed(self):
        try:
            return ast.parse(self.contents)
        except SyntaxError:
            warnings.warn(f'Could not parse {self.path} due to SyntaxError')
            return None

    @cached_property
    def contents(self) -> str:
        with open(self.path, encoding='utf8') as f:
            file_contents = f.read()
        return file_contents

    @cached_property
    def docstring(self) -> Optional[str]:
        if self.parsed is None:
            return None
        return ast.get_docstring(self.parsed)
