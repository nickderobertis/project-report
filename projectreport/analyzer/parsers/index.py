from projectreport.analyzer.parsers.javascript import PackageJSONParser
from projectreport.analyzer.parsers.python.init import PythonInitParser
from projectreport.analyzer.parsers.python.setup_py import PythonSetupParser

PARSER_EXTENSIONS = {"py": PythonInitParser}

PARSER_DOC_FILES = {
    "__init__.py": PythonInitParser,
    "setup.py": PythonSetupParser,
    "package.json": PackageJSONParser,
}
