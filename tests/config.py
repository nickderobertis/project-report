from pathlib import Path

GITHUB_REPO_URL = "https://github.com/nickderobertis/github-project-example"
TESTS_DIR = Path(__file__).parent
PROJECT_DIR = TESTS_DIR.parent
TEST_FILES_BASE_PATH = TESTS_DIR / "input_data"
PYTHON_PROJECT_NAME = "python_example"
PYTHON_PROJECT_PATH = TEST_FILES_BASE_PATH / PYTHON_PROJECT_NAME
JS_PROJECT_NAME = "js_example"
JS_PROJECT_PATH = TEST_FILES_BASE_PATH / JS_PROJECT_NAME
GIT_PROJECT_NAME = "git_example"
REPORTS_NAME = "reports"
REPORTS_FOLDER = TEST_FILES_BASE_PATH / REPORTS_NAME
