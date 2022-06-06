import datetime
from pathlib import Path

import git
import pytest
import pytz

from projectreport import Project
from tests.config import (
    GITHUB_REPO_URL,
    JS_PROJECT_PATH,
    PYTHON_DUNDER_VERSION_PROJECT_PATH,
    PYTHON_SETUP_CFG_VERSION_PROJECT_PATH,
    PYTHON_SETUP_PY_VERSION_PROJECT_PATH,
)
from tests.dirutils import create_temp_path


@pytest.fixture(scope="session")
def github_project_folder() -> Project:
    with create_temp_path() as temp_folder:
        project_path = temp_folder / "github-project-example"
        git.Repo.clone_from(GITHUB_REPO_URL, project_path)
        yield project_path


@pytest.fixture(scope="session")
def github_project(github_project_folder: Path) -> Project:
    project_path = github_project_folder
    included_types = None
    project = Project(project_path, included_types=included_types)
    yield project


def get_python_dunder_version_project() -> Project:
    project_path = PYTHON_DUNDER_VERSION_PROJECT_PATH
    included_types = ("py",)
    project = Project(project_path, included_types=included_types)
    return project


def get_python_setup_py_version_project() -> Project:
    project_path = PYTHON_SETUP_PY_VERSION_PROJECT_PATH
    included_types = ("py",)
    project = Project(project_path, included_types=included_types)
    return project


def get_python_setup_cfg_version_project() -> Project:
    project_path = PYTHON_SETUP_CFG_VERSION_PROJECT_PATH
    included_types = ("py", "cfg")
    project = Project(project_path, included_types=included_types)
    return project


def get_js_project() -> Project:
    project_path = JS_PROJECT_PATH
    included_types = ("js",)
    project = Project(project_path, included_types=included_types)
    return project


@pytest.fixture(scope="session")
def git_project() -> Project:
    with create_temp_path() as base_dir:
        d = base_dir / "gitrepo"
        r = git.Repo.init(d)
        # This function just creates an empty file ...
        (d / "tempfile").write_text("woo")
        r.index.add(["tempfile"])
        r.index.commit("initial commit")
        included_types = None
        project = Project(d, included_types=included_types)
        eastern = pytz.timezone("US/Eastern")
        project.data["created"] = datetime.datetime(
            2020, 2, 1, 12, 0, 0, 0, tzinfo=eastern
        )
        project.data["updated"] = datetime.datetime(
            2020, 2, 1, 12, 1, 0, 0, tzinfo=eastern
        )
        assert project.path == str(d)
        yield project
