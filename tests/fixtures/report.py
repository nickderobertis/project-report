from typing import Optional, Sequence

from projectreport import Project, Report
from tests.fixtures.project import get_python_dunder_version_project


def get_project_report(add_projects: Optional[Sequence[Project]] = None) -> Report:
    py_project = get_python_dunder_version_project()

    projects = [
        py_project,
    ]

    if add_projects:
        projects.extend(add_projects)

    report = Report(projects)
    return report
