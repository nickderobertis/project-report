from projectreport.analyzer.parsers.javascript import PackageJSONParser
from projectreport.analyzer.parsers.python.init import PythonParser

PARSER_EXTENSIONS = {"py": PythonParser}

PARSER_DOC_FILES = {
    "__init__.py": PythonParser,
    "package.json": PackageJSONParser,
}
