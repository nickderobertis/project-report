from typing import Optional, List, Sequence
import os

from cached_property import cached_property
from projectreport.analyzer.analysis import FolderAnalysis
from projectreport.analyzer.module import Module


class Folder:

    def __init__(self, path: str, root_path: Optional[str] = None, excluded_types: Optional[Sequence[str]] = None,
                 included_types: Optional[Sequence[str]] = None):
        self.path = os.path.abspath(path)
        self.name = os.path.basename(path)
        if root_path is None:
            root_path = self.name
        self.root_path = root_path
        self.options = dict(
            excluded_types=excluded_types,
            included_types=included_types
        )
        self._validate()

    @cached_property
    def file_paths(self) -> List[str]:
        file_names = [file for file in next(os.walk(self.path))[2]]
        included_files = []
        for file in file_names:
            extension = os.path.splitext(file)[1].strip('.')
            if self.options['included_types']:
                if extension in self.options['included_types']:
                    included_files.append(file)
            elif self.options['excluded_types']:
                if extension not in self.options['excluded_types']:
                    included_files.append(file)
            else:
                # No included or excluded files, just keep all
                included_files.append(file)
        files = [os.path.join(self.path, name) for name in included_files]
        return files

    @cached_property
    def folder_paths(self) -> List[str]:
        folders = [file for file in next(os.walk(self.path))[1]]
        abs_folders = [os.path.join(self.path, folder) for folder in folders]
        return abs_folders

    @cached_property
    def modules(self) -> List['Module']:
        return [Module(file_path, self.path) for file_path in self.file_paths]

    @cached_property
    def folders(self) -> List['Folder']:
        return [self.__class__(folder, root_path=self.root_path, **self.options) for folder in self.folder_paths]

    @cached_property
    def source_analysis(self) -> 'FolderAnalysis':
        analysis = FolderAnalysis()
        for folder in self.folders:
            analysis.add_subfolder_analysis(folder.source_analysis)
        for module in self.modules:
            analysis.add_module_analysis(module.source_analysis)
        return analysis

    def _validate(self):
        if self.options['included_types'] and self.options['excluded_types']:
            raise ValueError('cannot pass both include and exclude types')
