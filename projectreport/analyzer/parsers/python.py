import ast
import os
from cached_property import cached_property
from projectreport.analyzer.parsers.base import Parser


class PythonParser(Parser):

    @cached_property
    def parsed(self):
        return ast.parse(self.contents)

    @cached_property
    def contents(self):
        with open(self.path) as f:
            file_contents = f.read()
        return file_contents

    @cached_property
    def docstring(self):
        print(f'docstring for {self.path}: {ast.get_docstring(self.parsed)}')
        return ast.get_docstring(self.parsed)
