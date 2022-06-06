import ast
import warnings

from cached_property import cached_property

from projectreport.analyzer.parsers.file import SingleFileParser


class PythonParser(SingleFileParser):
    @cached_property
    def parsed(self):
        try:
            return ast.parse(self.contents)
        except SyntaxError:
            warnings.warn(f"Could not parse {self.path} due to SyntaxError")
            return None
