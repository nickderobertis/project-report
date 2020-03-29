import os

from tests.base import PYTHON_PROJECT_PATH, PYTHON_PROJECT_NAME, get_python_project, get_git_project


def test_python_project():
    project = get_python_project()

    assert project.file_names == ['__init__.py']
    assert project.file_paths == [os.path.abspath(os.path.join(PYTHON_PROJECT_PATH, '__init__.py'))]
    assert project.docstring == 'An example Python package for testing purposes'
    assert project.name == PYTHON_PROJECT_NAME
    assert project.path == os.path.abspath(PYTHON_PROJECT_PATH)
    assert project.repo is None
    assert not project.is_empty
    assert project.folders == []
    # TODO [#6]: test python project .analysis, .modules, .data


def test_git_project():
    project = get_git_project()

    assert project.repo is not None
    # TODO [#7]: better testing of git project