import importlib.util
from types import ModuleType
from typing import Optional
import ast
import warnings
from cached_property import cached_property
from getversion import get_module_version
from getversion.main import get_version_using_pkgresources, ModuleVersionNotFound
from getversion.plugin_builtins import get_builtin_module_version
from getversion.plugin_eggs_and_wheels import get_unzipped_wheel_or_egg_version
from getversion.plugin_importlib_metadata import get_version_using_importlib_metadata

from projectreport.analyzer.parsers.base import Parser


class PythonParser(Parser):
    @cached_property
    def parsed(self):
        try:
            return ast.parse(self.contents)
        except SyntaxError:
            warnings.warn(f"Could not parse {self.path} due to SyntaxError")
            return None

    @cached_property
    def docstring(self) -> Optional[str]:
        if self.parsed is None:
            return None
        return ast.get_docstring(self.parsed)

    @cached_property
    def module(self) -> ModuleType:
        spec = importlib.util.spec_from_file_location(self.file_name, self.path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    @cached_property
    def version(self) -> Optional[str]:
        try:
            version, details = get_module_version(
                self.module,
                rootmodule_strategies=(
                    get_version_using_pkgresources,
                    get_builtin_module_version,
                    get_version_using_importlib_metadata,
                    get_unzipped_wheel_or_egg_version,
                    # get_version_using_setuptools_scm,  # was returning invalid results
                ),
            )
        except ModuleVersionNotFound as e:
            raise e
            return None
        return version
