from typing import TYPE_CHECKING, Dict, Union, Sequence
from cached_property import cached_property
if TYPE_CHECKING:
    from projectreport.analyzer.project import Project
from projectreport.report.project import ProjectReport
from projectreport.report.base import BaseReport


class Report(BaseReport):
    """
    Pass Projects to create a report of the analysis of the projects.
    """

    def __init__(self, projects: Sequence['Project'], depth: int = 0):
        self.project_reports = [ProjectReport(project, depth=depth) for project in projects]

    @cached_property
    def data(self):
        return [report.data for report in self.project_reports]

    @cached_property
    def doc(self):
        from projectreport.report.latex import multi_project_latex_document
        return multi_project_latex_document(self.data)

