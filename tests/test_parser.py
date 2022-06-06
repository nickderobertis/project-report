from pathlib import Path

from projectreport.analyzer.parsers.github import GithubParser
from projectreport.analyzer.parsers.multi.file import MultiFileParser
from projectreport.analyzer.parsers.multi.main import MainMultiParser
from projectreport.analyzer.parsers.python.init import PythonInitParser
from projectreport.analyzer.parsers.python.setup_cfg import PythonSetupCfgParser
from projectreport.analyzer.parsers.python.setup_py import PythonSetupPyParser
from projectreport.version import Version
from tests.config import (
    GITHUB_REPO_URL,
    PYTHON_DUNDER_VERSION_PROJECT_PATH,
    PYTHON_SETUP_CFG_VERSION_PROJECT_PATH,
    PYTHON_SETUP_PY_VERSION_PROJECT_PATH,
)
from tests.fixtures.temp_dir import temp_folder


def test_init_py_parser():
    input_file = PYTHON_DUNDER_VERSION_PROJECT_PATH / "__init__.py"
    assert PythonInitParser.matches_path(input_file)
    parser = PythonInitParser(input_file)
    assert parser.docstring == "An example Python package for testing purposes"
    assert parser.version == Version.from_str("0.0.1")


def test_setup_py_parser():
    input_file = PYTHON_SETUP_PY_VERSION_PROJECT_PATH / "setup.py"
    assert PythonSetupPyParser.matches_path(input_file)
    parser = PythonSetupPyParser(input_file)
    assert (
        parser.docstring
        == "[from setup.py] An example Python package for testing purposes (version from setup.py)"
    )
    assert parser.version == Version.from_str("0.0.1")


def test_setup_cfg_parser():
    input_file = PYTHON_SETUP_CFG_VERSION_PROJECT_PATH / "setup.cfg"
    assert PythonSetupCfgParser.matches_path(input_file)
    parser = PythonSetupCfgParser(input_file)
    assert (
        parser.docstring
        == "[from setup.cfg] An example Python package for testing purposes (version from setup.cfg)"
    )
    assert parser.version == Version.from_str("1.0.0")


def test_github_parser():
    url = GITHUB_REPO_URL
    assert GithubParser.matches_path(url)
    parser = GithubParser(url)
    assert parser.docstring == "Example Github Project for project-report tests"
    assert parser.version == Version.from_str("1.0.0")


def test_multi_file_parser():
    input_folder = PYTHON_SETUP_CFG_VERSION_PROJECT_PATH
    input_files = ["__init__.py", "setup.cfg"]
    assert MultiFileParser.matches_path(input_folder, input_files)
    parser = MultiFileParser(input_folder, input_files)
    assert (
        parser.docstring
        == "[from __init__.py] An example Python package for testing purposes (version from setup.cfg)"
    )
    assert parser.version == Version.from_str("1.0.0")


# TODO: additional tests for main multi parser


def test_main_multi_parser_on_folder():
    input_folder = PYTHON_SETUP_CFG_VERSION_PROJECT_PATH
    input_files = ["__init__.py", "setup.cfg"]
    assert MainMultiParser.matches_path(input_folder, input_files)
    parser = MainMultiParser(input_folder, input_files)
    assert (
        parser.docstring
        == "[from __init__.py] An example Python package for testing purposes (version from setup.cfg)"
    )
    assert parser.version == Version.from_str("1.0.0")


def test_main_multi_parser_on_urls(temp_folder: Path):
    input_folder = str(temp_folder)
    input_files = []
    urls = [GITHUB_REPO_URL]
    assert MainMultiParser.matches_path(input_folder, input_files, urls)
    parser = MainMultiParser(input_folder, input_files, urls)
    assert parser.docstring == "Example Github Project for project-report tests"
    assert parser.version == Version.from_str("1.0.0")
