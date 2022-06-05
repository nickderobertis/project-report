from pathlib import Path
from typing import Final, List

GITHUB_REPO_URL = "https://github.com/nickderobertis/github-project-example"
TESTS_DIR = Path(__file__).parent
PROJECT_DIR = TESTS_DIR.parent
TEST_FILES_BASE_PATH = TESTS_DIR / "input_data"

PYTHON_EXAMPLES_FOLDER = TEST_FILES_BASE_PATH / "python_examples"
PYTHON_DUNDER_VERSION_PROJECT_NAME = "dunder_version"
PYTHON_DUNDER_VERSION_PROJECT_PATH = (
    PYTHON_EXAMPLES_FOLDER / PYTHON_DUNDER_VERSION_PROJECT_NAME
)
PYTHON_SETUP_PY_VERSION_PROJECT_NAME = "setup_py"
PYTHON_SETUP_PY_VERSION_PROJECT_PATH = (
    PYTHON_EXAMPLES_FOLDER / PYTHON_SETUP_PY_VERSION_PROJECT_NAME
)
PYTHON_SETUP_CFG_VERSION_PROJECT_NAME = "setup_cfg"
PYTHON_SETUP_CFG_VERSION_PROJECT_PATH = (
    PYTHON_EXAMPLES_FOLDER / PYTHON_SETUP_CFG_VERSION_PROJECT_NAME
)
PYTHON_PROJECT_PATHS: Final[List[str]] = sorted(
    [
        str(PYTHON_DUNDER_VERSION_PROJECT_PATH),
        str(PYTHON_SETUP_PY_VERSION_PROJECT_PATH),
        str(PYTHON_SETUP_CFG_VERSION_PROJECT_PATH),
    ]
)

JS_PROJECT_NAME = "js_example"
JS_PROJECT_PATH = TEST_FILES_BASE_PATH / JS_PROJECT_NAME

GIT_PROJECT_NAME = "git_example"

REPORTS_NAME = "reports"
REPORTS_FOLDER = TEST_FILES_BASE_PATH / REPORTS_NAME
