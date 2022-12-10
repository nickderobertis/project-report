import datetime
import os

import pytz
from git import Repo

from projectreport import Project
from projectreport.analyzer.analysis import FolderAnalysis
from projectreport.license.model import LicenseType
from projectreport.version import Version
from tests.config import (
    JS_PROJECT_NAME,
    JS_PROJECT_PATH,
    PYTHON_DUNDER_VERSION_PROJECT_NAME,
    PYTHON_DUNDER_VERSION_PROJECT_PATH,
    PYTHON_SETUP_CFG_VERSION_PROJECT_NAME,
    PYTHON_SETUP_CFG_VERSION_PROJECT_PATH,
    PYTHON_SETUP_PY_VERSION_PROJECT_NAME,
    PYTHON_SETUP_PY_VERSION_PROJECT_PATH,
)
from tests.fixtures.project import (
    get_js_project,
    get_python_dunder_version_project,
    get_python_setup_cfg_version_project,
    get_python_setup_py_version_project,
    git_project,
    github_project,
    github_project_folder,
)
from tests.github_stub import patch_github


def test_python_dunder_version_project():
    project = get_python_dunder_version_project()

    assert sorted(project.file_names) == ["LICENSE.md", "__init__.py"]
    assert project.file_paths == [
        os.path.abspath(os.path.join(PYTHON_DUNDER_VERSION_PROJECT_PATH, "__init__.py"))
    ]
    assert project.docstring == "An example Python package for testing purposes"
    assert project.version == Version.from_str("0.0.1")
    assert project.topics is None
    assert project.name == PYTHON_DUNDER_VERSION_PROJECT_NAME
    assert project.path == os.path.abspath(PYTHON_DUNDER_VERSION_PROJECT_PATH)
    assert project.repo is None
    assert not project.is_empty
    assert project.folders == []

    analysis: FolderAnalysis = project.analysis
    assert analysis.lines == {"code": 2, "documentation": 3, "empty": 0, "string": 0}
    assert len(project.modules) == 1
    assert project.modules[0].name == "__init__"
    assert project.data["num_commits"] == None
    assert project.data["created"] == None
    assert project.data["updated"] == None
    assert project.data["lines"] == 2
    assert project.data["full_lines"] == 5
    assert project.data["urls"] == None
    assert project.data["docstring"] == "An example Python package for testing purposes"
    assert project.data["version"] == "0.0.1"
    assert project.data["name"] == PYTHON_DUNDER_VERSION_PROJECT_NAME
    assert project.data["topics"] == None
    assert project.data["license"] == "MIT"

    assert project.license is not None
    assert project.license.type == LicenseType.MIT


def test_python_setup_py_version_project():
    project = get_python_setup_py_version_project()

    assert sorted(project.file_names) == ["COPYING", "__init__.py", "setup.py"]
    assert sorted(project.file_paths) == [
        os.path.abspath(
            os.path.join(PYTHON_SETUP_PY_VERSION_PROJECT_PATH, "__init__.py")
        ),
        os.path.abspath(os.path.join(PYTHON_SETUP_PY_VERSION_PROJECT_PATH, "setup.py")),
    ]
    assert (
        project.docstring
        == "[from __init__.py] An example Python package for testing purposes (version from setup.py)"
    )
    assert project.version == Version.from_str("0.0.1")
    assert sorted(project.topics) == [
        "Application Frameworks",
        "Libraries",
        "Software Development",
        "Testing",
    ]
    assert project.name == PYTHON_SETUP_PY_VERSION_PROJECT_NAME
    assert project.path == os.path.abspath(PYTHON_SETUP_PY_VERSION_PROJECT_PATH)
    assert project.repo is None
    assert not project.is_empty
    assert project.folders == []

    analysis: FolderAnalysis = project.analysis
    assert analysis.lines == {"code": 10, "documentation": 3, "empty": 3, "string": 6}
    assert len(project.modules) == 2
    module_names = [module.name for module in project.modules]
    assert "__init__" in module_names
    assert "setup" in module_names
    assert project.data["num_commits"] == None
    assert project.data["created"] == None
    assert project.data["updated"] == None
    assert project.data["lines"] == 10
    assert project.data["full_lines"] == 22
    assert project.data["urls"] == None
    assert (
        project.data["docstring"]
        == "[from __init__.py] An example Python package for testing purposes (version from setup.py)"
    )
    assert project.data["version"] == "0.0.1"
    assert project.data["name"] == PYTHON_SETUP_PY_VERSION_PROJECT_NAME
    assert sorted(project.data["topics"]) == [
        "Application Frameworks",
        "Libraries",
        "Software Development",
        "Testing",
    ]
    assert project.data["license"] == "GPL"

    assert project.license is not None
    assert project.license.type == LicenseType.GPL


def test_python_setup_cfg_version_project():
    project = get_python_setup_cfg_version_project()

    assert sorted(project.file_names) == ["__init__.py", "license.txt", "setup.cfg"]
    assert sorted(project.file_paths) == [
        os.path.abspath(
            os.path.join(PYTHON_SETUP_CFG_VERSION_PROJECT_PATH, "__init__.py")
        ),
        os.path.abspath(
            os.path.join(PYTHON_SETUP_CFG_VERSION_PROJECT_PATH, "setup.cfg")
        ),
    ]
    assert (
        project.docstring
        == "[from __init__.py] An example Python package for testing purposes (version from setup.cfg)"
    )
    assert project.version == Version.from_str("1.0.0")
    assert sorted(project.topics) == [
        "Libraries",
        "Python Modules",
        "Software Development",
        "Testing",
        "Utilities",
    ]
    assert project.name == PYTHON_SETUP_CFG_VERSION_PROJECT_NAME
    assert project.path == os.path.abspath(PYTHON_SETUP_CFG_VERSION_PROJECT_PATH)
    assert project.repo is None
    assert not project.is_empty
    assert project.folders == []

    analysis: FolderAnalysis = project.analysis
    assert analysis.lines == {"code": 16, "documentation": 3, "empty": 0, "string": 0}
    assert len(project.modules) == 2
    module_names = [module.name for module in project.modules]
    assert "__init__" in module_names
    assert "setup" in module_names
    assert project.data["num_commits"] == None
    assert project.data["created"] == None
    assert project.data["updated"] == None
    assert project.data["lines"] == 16
    assert project.data["full_lines"] == 19
    assert project.data["urls"] == None
    assert (
        project.data["docstring"]
        == "[from __init__.py] An example Python package for testing purposes (version from setup.cfg)"
    )
    assert project.data["version"] == "1.0.0"
    assert project.data["name"] == PYTHON_SETUP_CFG_VERSION_PROJECT_NAME
    assert sorted(project.data["topics"]) == [
        "Libraries",
        "Python Modules",
        "Software Development",
        "Testing",
        "Utilities",
    ]
    assert project.data["license"] == "APACHE"

    assert project.license is not None
    assert project.license.type == LicenseType.APACHE


def test_javascript_project():
    project = get_js_project()

    assert sorted(project.file_names) == ["index.js", "package.json"]
    assert project.file_paths == [
        os.path.abspath(os.path.join(JS_PROJECT_PATH, "index.js")),
    ]
    assert project.docstring == "An example JavaScript package"
    assert project.version == Version.from_str("1.0.0")
    assert project.topics == ["kwd1", "kwd2"]
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
        "topics": ["kwd1", "kwd2"],
        "license": None,
    }

    assert project.license is None


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


@patch_github()
def test_github_project(github_project: Project):
    project = github_project

    assert isinstance(project.repo, Repo)
    assert project.name == "github-project-example"
    assert project.docstring == "Github repo stub description"
    assert project.version == Version.from_str("1.0.0")
    assert project.topics == ["stub-topic1", "stub-topic2"]
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
    assert data["topics"] == ["stub-topic1", "stub-topic2"]
