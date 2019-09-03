from typing import TYPE_CHECKING, Dict, Union
if TYPE_CHECKING:
    from projectreport.analyzer.project import Project
    from projectreport.analyzer.folder import Folder
from cached_property import cached_property
import yaml
from projectreport.report.json import to_json


class ProjectReport:

    def __init__(self, project: 'Project', depth: int = 0):
        self.project = project
        self.depth = depth

    def __str__(self):
        return self.yaml

    @cached_property
    def json(self) -> str:
        return to_json(self.data)

    @cached_property
    def yaml(self) -> str:
        return yaml.dump(self.data, indent=2)

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




