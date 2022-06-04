from pathlib import Path

from cached_property import cached_property


class Parser:

    def __init__(self, path: str):
        self.path = path

    @cached_property
    def parsed(self):
        raise NotImplementedError

    @cached_property
    def contents(self) -> str:
        with open(self.path, encoding='utf8') as f:
            file_contents = f.read()
        return file_contents

    @cached_property
    def docstring(self):
        raise NotImplementedError

    @cached_property
    def version(self):
        raise NotImplementedError

    @cached_property
    def file_name(self) -> str:
        return Path(self.path).with_suffix('').name

