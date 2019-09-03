from typing import Optional, List, Sequence, TYPE_CHECKING
if TYPE_CHECKING:
    from projectreport.analyzer.project import Project
    from projectreport.analyzer.parsers.base import Parser
import os

from cached_property import cached_property
from projectreport.analyzer.analysis import FolderAnalysis
from projectreport.analyzer.module import Module
from projectreport.analyzer.analyzable import Analyzable
from projectreport.analyzer.parsers.index import PARSER_DOC_FILES


class Folder(Analyzable):

    def __init__(self, path: str, project: Optional['Project'] = None, excluded_types: Optional[Sequence[str]] = None,
                 included_types: Optional[Sequence[str]] = None):
        from projectreport.analyzer.project import Project
        path = os.path.abspath(path)
        self.name = os.path.basename(path)
        self.options = dict(
            excluded_types=excluded_types,
            included_types=included_types
        )
        if project is None:
            project = Project(self.path, **self.options)
        self._validate()
        super().__init__(path, project=project)

    @cached_property
    def file_names(self) -> List[str]:
        file_names = [file for file in next(os.walk(self.path))[2]]
        return file_names

    @cached_property
    def file_paths(self) -> List[str]:
        included_files = []
        for file in self.file_names:
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
        return [Module(file_path, self.name, project=self.project) for file_path in self.file_paths]

    @cached_property
    def folders(self) -> List['Folder']:
        return [Folder(folder, project=self.project, **self.options) for folder in self.folder_paths]

    @cached_property
    def analysis(self) -> 'FolderAnalysis':
        analysis = FolderAnalysis(self)
        for folder in self.folders:
            analysis.add_subfolder_analysis(folder.analysis)
        for module in self.modules:
            analysis.add_module_analysis(module.analysis)
        return analysis

    @cached_property
    def parser(self) -> Optional['Parser']:
        for file, parser in PARSER_DOC_FILES.items():
            if file in self.file_names:
                full_path = os.path.join(self.path, file)
                return PARSER_DOC_FILES[file](full_path)
        return None

    def _validate(self):
        if self.options['included_types'] and self.options['excluded_types']:
            raise ValueError('cannot pass both include and exclude types')
