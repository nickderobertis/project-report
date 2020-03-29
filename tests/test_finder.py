from projectreport.finder.combine import CombinedFinder
from projectreport.finder.git import GitFinder
from projectreport.finder.python import PythonPackageFinder
from tests.base import TEST_FILES_BASE_PATH, PYTHON_PROJECT_PATH


def test_find_python_package():
    finder = PythonPackageFinder()
    search_paths = [
        TEST_FILES_BASE_PATH
    ]
    project_paths = finder.find_all(search_paths)
    assert project_paths == [PYTHON_PROJECT_PATH]


def test_find_git_package():
    finder = GitFinder()
    search_paths = [
        '.'
    ]
    project_paths = finder.find_all(search_paths)
    assert project_paths == ['.']


def test_combined_finder():
    finder = CombinedFinder([
        GitFinder(),
        PythonPackageFinder()
    ])
    search_paths = [
        TEST_FILES_BASE_PATH
    ]
    project_paths = finder.find_all(search_paths)
    assert project_paths == [PYTHON_PROJECT_PATH]
