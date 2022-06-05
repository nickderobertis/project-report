import datetime
from typing import TYPE_CHECKING, Callable, Dict, List, Optional, Sequence, Union

from cached_property import cached_property

if TYPE_CHECKING:
    from projectreport.analyzer.project import Project

from projectreport.report.base import BaseReport
from projectreport.report.project import ProjectReport


class Report(BaseReport):
    """
    Pass Projects to create a report of the analysis of the projects.
    """

    def __init__(self, projects: Sequence["Project"], depth: int = 0):
        self.project_reports = [
            ProjectReport(project, depth=depth) for project in projects
        ]

    @cached_property
    def data(self) -> List[dict]:
        items = [report.data for report in self.project_reports]
        items.sort(key=_created_then_name_key)
        return items

    @cached_property
    def doc(self):
        from projectreport.report.latex import multi_project_latex_document

        return multi_project_latex_document(self.data)

    def sort(self, key: Optional[Callable[[dict], str]] = None, reverse: bool = False):
        self.data.sort(key=key, reverse=reverse)

    def default_sort(self):
        self.data.sort(key=_created_then_name_key)


def _created_then_name_key(data: dict) -> str:
    created: Optional[datetime.datetime] = data["created"]
    if created is None:
        created_str = "0000-00-00 00:00:00.000000"
    else:
        created_str = created.strftime("%Y-%m-%d %H:%M:%S.%f")

    name: str = data["name"]
    return f"{created_str}_{name}"
