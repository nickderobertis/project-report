import datetime
import os

import pytz
from git import Repo

from projectreport import Project
from projectreport.analyzer.analysis import FolderAnalysis
from projectreport.version import Version
from tests.config import (
    JS_PROJECT_NAME,
    JS_PROJECT_PATH,
    PYTHON_PROJECT_NAME,
    PYTHON_PROJECT_PATH,
)
from tests.fixtures.project import (
    get_js_project,
    get_python_project,
    git_project,
    github_project,
)


def test_python_project():
    project = get_python_project()

    assert project.file_names == ["__init__.py"]
    assert project.file_paths == [
        os.path.abspath(os.path.join(PYTHON_PROJECT_PATH, "__init__.py"))
    ]
    assert project.docstring == "An example Python package for testing purposes"
    assert project.version == Version.from_str("0.0.1")
    assert project.name == PYTHON_PROJECT_NAME
    assert project.path == os.path.abspath(PYTHON_PROJECT_PATH)
    assert project.repo is None
    assert not project.is_empty
    assert project.folders == []

    analysis: FolderAnalysis = project.analysis
    assert analysis.lines == {"code": 2, "documentation": 3, "empty": 0, "string": 0}
    assert len(project.modules) == 1
    assert project.modules[0].name == "__init__"
    assert project.data == {
        "num_commits": None,
        "created": None,
        "updated": None,
        "lines": 2,
        "full_lines": 5,
        "urls": None,
        "docstring": "An example Python package for testing purposes",
        "version": "0.0.1",
        "name": PYTHON_PROJECT_NAME,
    }


def test_javascript_project():
    project = get_js_project()

    assert sorted(project.file_names) == ["index.js", "package.json"]
    assert project.file_paths == [
        os.path.abspath(os.path.join(JS_PROJECT_PATH, "index.js")),
    ]
    assert project.docstring == "An example JavaScript package"
    assert project.version == Version.from_str("1.0.0")
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
        "version": "1.0.0",
        "name": "js_example",
    }


def test_git_project(git_project: Project):
    project = git_project

    assert project.name == "gitrepo"
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


def test_github_project(github_project: Project):
    project = github_project

    assert isinstance(project.repo, Repo)
    assert project.name == "github-project-example"
    assert project.docstring == "Example Github Project for project-report tests"
    assert project.version == Version.from_str("1.0.0")
    assert not project.repo is None
    assert not project.is_empty
    assert project.folders == []
    analysis: FolderAnalysis = project.analysis
    assert analysis.lines["code"] == 18
    assert analysis.lines["documentation"] == 0
    assert analysis.lines["empty"] == 4
    assert analysis.lines["string"] == 0
    data = project.data
    assert data["urls"] == ["https://github.com/nickderobertis/github-project-example"]
