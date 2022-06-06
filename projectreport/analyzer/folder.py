from pathlib import Path
from typing import TYPE_CHECKING, List, Optional, Sequence, Union

from projectreport.analyzer.parsers.github import GithubParser
from projectreport.analyzer.parsers.multi.file import MultiFileParser
from projectreport.analyzer.parsers.multi.main import MainMultiParser
from projectreport.logger import logger

if TYPE_CHECKING:
    from projectreport.analyzer.project import Project
    from projectreport.analyzer.parsers.base import Parser

import os

from cached_property import cached_property

from projectreport.analyzer.analysis import FolderAnalysis
from projectreport.analyzer.analyzable import Analyzable
from projectreport.analyzer.module import Module
from projectreport.analyzer.parsers.index import PARSER_DOC_FILES
from projectreport.config import DEFAULT_IGNORE_PATHS
from projectreport.tools.expand_glob import all_possible_paths


class Folder(Analyzable):
    def __init__(
        self,
        path: Union[str, Path],
        project: Optional["Project"] = None,
        excluded_types: Optional[Sequence[str]] = None,
        included_types: Optional[Sequence[str]] = None,
        ignore_paths: Optional[Sequence[str]] = DEFAULT_IGNORE_PATHS,
    ):
        from projectreport.analyzer.project import Project

        path = os.path.abspath(path)
        self.name = os.path.basename(path)
        self.options = dict(
            excluded_types=excluded_types,
            included_types=included_types,
            ignore_paths=ignore_paths,
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
        if self.options["ignore_paths"] is not None:
            all_ignore_paths = all_possible_paths(
                self.options["ignore_paths"], self.path
            )

        for file in self.file_names:
            if self.options["ignore_paths"]:
                file_path = os.path.join(self.path, file)
                if file_path in all_ignore_paths:
                    continue  # this file excluded, skip it
            extension = os.path.splitext(file)[1].strip(".")
            if self.options["included_types"] is not None:
                if extension in self.options["included_types"]:
                    included_files.append(file)
            elif self.options["excluded_types"] is not None:
                if extension not in self.options["excluded_types"]:
                    included_files.append(file)
            else:
                # No included or excluded files, just keep all
                included_files.append(file)
        files = [os.path.join(self.path, name) for name in included_files]
        return files

    @cached_property
    def folder_paths(self) -> List[str]:
        folders = [file for file in next(os.walk(self.path))[1]]

        if self.options["ignore_paths"] is not None:
            all_ignore_paths = all_possible_paths(
                self.options["ignore_paths"], self.path
            )

        out_folders = []
        for folder in folders:
            abs_folder = os.path.join(self.path, folder)
            if self.options["ignore_paths"] is not None:
                if abs_folder in all_ignore_paths:
                    continue  # this folder excluded, skip it
            out_folders.append(abs_folder)

        return out_folders

    @cached_property
    def modules(self) -> List["Module"]:
        return [
            Module(file_path, self.name, project=self.project)
            for file_path in self.file_paths
        ]

    @cached_property
    def folders(self) -> List["Folder"]:
        all_folders = [
            Folder(folder, project=self.project, **self.options)
            for folder in self.folder_paths
        ]
        non_empty_folders = [folder for folder in all_folders if not folder.is_empty]
        return non_empty_folders

    @cached_property
    def analysis(self) -> "FolderAnalysis":
        analysis = FolderAnalysis(self)
        for folder in self.folders:
            logger.debug(f"Analyzing folder {folder.name}")
            analysis.add_subfolder_analysis(folder.analysis)
        for module in self.modules:
            logger.debug(f"Analyzing module {module.name}")
            analysis.add_module_analysis(module.analysis)
        return analysis

    @cached_property
    def parser(self) -> Optional["Parser"]:
        if not MainMultiParser.matches_path(
            self.path, self.file_names, self.analysis.data.get("urls")
        ):
            return None
        return MainMultiParser(
            self.path, self.file_names, self.analysis.data.get("urls")
        )

    @cached_property
    def is_empty(self) -> bool:
        len_contents = len(self.file_paths) + len(self.folders)
        return len_contents == 0

    def _validate(self):
        if self.options["included_types"] and self.options["excluded_types"]:
            raise ValueError("cannot pass both include and exclude types")
