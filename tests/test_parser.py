from projectreport.analyzer.parsers.python.init import PythonInitParser
from projectreport.analyzer.parsers.python.setup_cfg import PythonSetupCfgParser
from projectreport.analyzer.parsers.python.setup_py import PythonSetupPyParser
from projectreport.version import Version
from tests.config import (
    PYTHON_DUNDER_VERSION_PROJECT_PATH,
    PYTHON_SETUP_CFG_VERSION_PROJECT_PATH,
    PYTHON_SETUP_PY_VERSION_PROJECT_PATH,
)


def test_init_py_parser():
    input_file = PYTHON_DUNDER_VERSION_PROJECT_PATH / "__init__.py"
    parser = PythonInitParser(input_file)
    assert parser.docstring == "An example Python package for testing purposes"
    assert parser.version == Version.from_str("0.0.1")


def test_setup_py_parser():
    input_file = PYTHON_SETUP_PY_VERSION_PROJECT_PATH / "setup.py"
    parser = PythonSetupPyParser(input_file)
    assert (
        parser.docstring
        == "[from setup.py] An example Python package for testing purposes (version from setup.py)"
    )
    assert parser.version == Version.from_str("0.0.1")


def test_setup_cfg_parser():
    input_file = PYTHON_SETUP_CFG_VERSION_PROJECT_PATH / "setup.cfg"
    parser = PythonSetupCfgParser(input_file)
    assert (
        parser.docstring
        == "[from setup.cfg] An example Python package for testing purposes (version from setup.cfg)"
    )
    assert parser.version == Version.from_str("1.0.0")
