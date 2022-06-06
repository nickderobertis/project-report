from cached_property import cached_property


class Parser:
    def __init__(self, path: str):
        self.path = path

    @cached_property
    def docstring(self):
        raise NotImplementedError

    @cached_property
    def version(self):
        raise NotImplementedError
