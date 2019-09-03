from typing import TYPE_CHECKING, Dict, Union
if TYPE_CHECKING:
    from projectreport.analyzer.project import Project
    from projectreport.analyzer.folder import Folder
from cached_property import cached_property
from projectreport.report.base import BaseReport


class ProjectReport(BaseReport):

    def __init__(self, project: 'Project', depth: int = 0):
        self.project = project
        self.depth = depth

    @cached_property
    def doc(self):
        from projectreport.report.latex import project_latex_document
        return project_latex_document(self.data)

    @cached_property
    def data(self) -> Dict[str, Union[str, int, dict]]:
        data = {}
        data.update(self.project.data)
        if self.depth == 0:
            return data

        data.update({'subprojects': {}})
        for folder in self.project.folders:
            folder_data = {}
            gather_data(folder, folder_data, remaining_depth=self.depth - 1)
            data['subprojects'][folder.path] = folder_data

        return data


def gather_data(folder: 'Folder', data: dict, remaining_depth: int = 0):
    data.update(folder.data)
    if remaining_depth <= 0:
        return

    data.update({'subprojects': {}})
    for folder in folder.folders:
        folder_data = {}
        gather_data(folder, folder_data, remaining_depth=remaining_depth - 1)
        data['subprojects'][folder.path] = folder_data




