import os
from pathlib import Path
from pprint import pprint

from projectreport import Project

specific_project_path_str = os.getenv("MANUAL_TESTING_PROJECT_PATH", ".")
specific_project_path = Path(specific_project_path_str)


def get_specific_project() -> Project:
    project_path = specific_project_path
    included_types = ("py",)
    project = Project(project_path, included_types=included_types)
    return project


if __name__ == "__main__":
    project = get_specific_project()
    pprint(project.data)
