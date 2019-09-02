from typing import List, Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from projectreport.analyzer.module import PythonModule
import os
from cached_property import cached_property

from projectreport.analyzer.analysis import PackageAnalysis


class PythonPackage:

    def __init__(self, path: str, root_package: Optional[str] = None):
        self.path = os.path.abspath(path)
        self.name = os.path.basename(path)
        if root_package is None:
            root_package = self.name
        self.root_package = root_package

    @cached_property
    def modules(self) -> List['PythonModule']:
        file_names = [file for file in next(os.walk(self.path))[2] if file.endswith('.py')]
        files = [os.path.join(self.path, name) for name in file_names]
        return [PythonModule(file, package=self.root_package) for file in files]

    @cached_property
    def packages(self) -> List['PythonPackage']:
        folders = [file for file in next(os.walk(self.path))[1]]
        abs_folders = [os.path.join(self.path, folder) for folder in folders]
        packages = [self.__class__(folder, root_package=self.root_package) for folder in abs_folders]
        return [package for package in packages if package.has_init]

    @cached_property
    def has_init(self) -> bool:
        return '__init__.py' in self.modules

    @cached_property
    def source_analysis(self) -> 'PackageAnalysis':
        analysis = PackageAnalysis()
        for package in self.packages:
            analysis.add_subpackage_analysis(package.source_analysis)
        for module in self.modules:
            analysis.add_module_analysis(module.source_analysis)
        return analysis