from pathlib import Path

import git
import pytest

from projectreport import Project
from tests.config import GITHUB_REPO_URL
from tests.dirutils import create_temp_path


@pytest.fixture(scope="session")
def github_project() -> Project:
    with create_temp_path() as temp_folder:
        project_path = temp_folder / "github-project-example"
        git.Repo.clone_from(GITHUB_REPO_URL, project_path)
        included_types = None
        project = Project(project_path, included_types=included_types)
        yield project
