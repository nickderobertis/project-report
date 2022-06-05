from projectreport.analyzer.parsers.javascript import PackageJSONParser
from projectreport.analyzer.parsers.python.init import PythonInitParser

PARSER_EXTENSIONS = {"py": PythonInitParser}

PARSER_DOC_FILES = {
    "__init__.py": PythonInitParser,
    "package.json": PackageJSONParser,
}
