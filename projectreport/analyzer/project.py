from typing import Optional
import os
from cached_property import cached_property


class Project:

    def __init__(self, path: str, name: Optional[str] = None):
        self.path = os.path.abspath(path)
        self.name = name if name is not None else os.path.basename(self.path)

