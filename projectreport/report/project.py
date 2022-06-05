from typing import TYPE_CHECKING, Dict, Union

from projectreport.data import AnalysisData

if TYPE_CHECKING:
    from projectreport.analyzer.project import Project
    from projectreport.analyzer.folder import Folder

from cached_property import cached_property

from projectreport.report.base import BaseReport


class ProjectReport(BaseReport):
    def __init__(self, project: "Project", depth: int = 0):
        self.project = project
        self.depth = depth

    @cached_property
    def doc(self):
        from projectreport.report.latex import project_latex_document

        return project_latex_document(self.data)

    @cached_property
    def data(self) -> AnalysisData:
        data: AnalysisData = {}
        data.update(self.project.data)
        if self.depth == 0:
            return data

        subprojects_dict: AnalysisData = {}
        for folder in self.project.folders:
            folder_data: AnalysisData = {}
            gather_data(folder, folder_data, remaining_depth=self.depth - 1)
            subprojects_dict[folder.path] = folder_data
        data.update({"subprojects": subprojects_dict})

        return data


def gather_data(folder: "Folder", data: dict, remaining_depth: int = 0):
    data.update(folder.data)
    if remaining_depth <= 0:
        return

    subprojects_dict: AnalysisData = {}
    for folder in folder.folders:
        folder_data: AnalysisData = {}
        gather_data(folder, folder_data, remaining_depth=remaining_depth - 1)
        subprojects_dict[folder.path] = folder_data
    data.update({"subprojects": subprojects_dict})
