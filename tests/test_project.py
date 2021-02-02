import datetime
import os

import pytz
from git import Repo

from projectreport import Project
from projectreport.analyzer.analysis import FolderAnalysis
from tests.base import (
    PYTHON_PROJECT_PATH,
    PYTHON_PROJECT_NAME,
    get_python_project,
    get_github_project,
    git_project, get_js_project, JS_PROJECT_PATH, JS_PROJECT_NAME,
)


def test_python_project():
    project = get_python_project()

    assert project.file_names == ["__init__.py"]
    assert project.file_paths == [
        os.path.abspath(os.path.join(PYTHON_PROJECT_PATH, "__init__.py"))
    ]
    assert project.docstring == "An example Python package for testing purposes"
    assert project.name == PYTHON_PROJECT_NAME
    assert project.path == os.path.abspath(PYTHON_PROJECT_PATH)
    assert project.repo is None
    assert not project.is_empty
    assert project.folders == []

    analysis: FolderAnalysis = project.analysis
    assert analysis.lines == {"code": 0, "documentation": 3, "empty": 0, "string": 0}
    assert len(project.modules) == 1
    assert project.modules[0].name == "__init__"
    assert project.data == {
        "num_commits": None,
        "created": None,
        "updated": None,
        "lines": 0,
        "full_lines": 3,
        "urls": None,
        "docstring": "An example Python package for testing purposes",
        "name": "python_example",
    }


def test_javascript_project():
    project = get_js_project()

    assert project.file_names == ["index.js", 'package.json']
    assert project.file_paths == [
        os.path.abspath(os.path.join(JS_PROJECT_PATH, "index.js")),
    ]
    assert project.docstring == "An example JavaScript package"
    assert project.name == JS_PROJECT_NAME
    assert project.path == os.path.abspath(JS_PROJECT_PATH)
    assert project.repo is None
    assert not project.is_empty
    assert project.folders == []

    analysis: FolderAnalysis = project.analysis
    assert analysis.lines == {"code": 1, "documentation": 0, "empty": 0, "string": 0}
    assert len(project.modules) == 1
    assert project.modules[0].name == "index"
    assert project.data == {
        "num_commits": None,
        "created": None,
        "updated": None,
        "lines": 1,
        "full_lines": 1,
        "urls": None,
        "docstring": "An example JavaScript package",
        "name": "js_example",
    }


def test_git_project(git_project: Project):
    project = git_project

    assert project.name == 'gitrepo'
    assert project.file_names == ["tempfile"]
    assert isinstance(project.repo, Repo)
    analysis: FolderAnalysis = project.analysis
    assert analysis.lines == {"code": 0, "documentation": 0, "empty": 0, "string": 0}
    assert len(project.modules) == 1
    assert project.modules[0].name == "tempfile"
    data = project.data
    assert data["num_commits"] == 1

    assert (data["created"] - datetime.datetime.now(pytz.utc)).total_seconds() < 180
    assert (data["updated"] - datetime.datetime.now(pytz.utc)).total_seconds() < 180


def test_github_project():
    project = get_github_project()

    assert isinstance(project.repo, Repo)
    assert project.name == "project-report"
    analysis: FolderAnalysis = project.analysis
    assert analysis.lines["code"] > 0
    assert analysis.lines["documentation"] > 0
    assert analysis.lines["empty"] > 0
    assert analysis.lines["string"] > 0
    data = project.data
    assert data["urls"] == ["https://github.com/nickderobertis/project-report"]
