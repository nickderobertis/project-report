import os
from pathlib import Path

import pytest
from tempfile import TemporaryDirectory
import git

from projectreport.analyzer.project import Project
from projectreport.report.report import Report

TEST_FILES_BASE_PATH = os.path.sep.join(['tests', 'input_data'])
PYTHON_PROJECT_NAME = 'python_example'
PYTHON_PROJECT_PATH = os.path.sep.join([TEST_FILES_BASE_PATH, PYTHON_PROJECT_NAME])
GIT_PROJECT_NAME = 'git_example'
REPORTS_NAME = 'reports'
REPORTS_FOLDER = os.path.join(TEST_FILES_BASE_PATH, REPORTS_NAME)


def get_python_project() -> Project:
    project_path = PYTHON_PROJECT_PATH
    included_types = ('py',)
    project = Project(project_path, included_types=included_types)
    return project


@pytest.fixture(scope='session')
def git_project() -> Project:
    with TemporaryDirectory() as d:
        r = git.Repo.init(d)
        # This function just creates an empty file ...
        (Path(d) / 'tempfile').write_text('woo')
        r.index.add(['tempfile'])
        r.index.commit("initial commit")
        included_types = None
        project = Project(d, included_types=included_types)
        assert project.name == Path(d).name
        assert project.path == d
        yield project


def get_github_project() -> Project:
    project_path = '.'
    included_types = None
    project = Project(project_path, included_types=included_types)
    return project


def get_project_report() -> Report:
    py_project = get_python_project()

    projects = [
        py_project
    ]

    report = Report(projects)
    return report

# TODO [#5]: include an example git repo for testing
#
# Need to determine how to include a .git folder inside a subfolder in the repo.
# Alternatively, use gitpython to create on the fly and delete at end of test