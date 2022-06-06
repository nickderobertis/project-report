import ast
from configparser import ConfigParser, ParsingError
from pathlib import Path
from typing import Optional

from cached_property import cached_property

from projectreport.analyzer.parsers.base import Parser
from projectreport.analyzer.parsers.python.base import PythonParser
from projectreport.version import Version

# NOTE: This does not use the PythonParser as a base class because this is not a Python file
# being parsed (it is an ini file with the cfg extension)


class PythonSetupCfgParser(Parser):
    @cached_property
    def parsed(self) -> Optional[ConfigParser]:
        # Try to load the file as an ini file using configparser
        try:
            config = ConfigParser()
            config.read(self.path)
            return config
        except ParsingError:
            return None

    @cached_property
    def docstring(self) -> Optional[str]:
        if self.parsed is None:
            return None

        # Return the description value from the metadata section, if it exists
        return _get_string_from_config(self.parsed, "metadata", "description")

    @cached_property
    def version(self) -> Optional[Version]:
        if self.parsed is None:
            return None

        # Return the version value from the metadata section, if it exists
        version_str = _get_string_from_config(self.parsed, "metadata", "version")
        if version_str is None:
            return None
        return Version.from_str(version_str)

    @classmethod
    def matches_path(cls, path: str) -> bool:
        return Path(path).name == "setup.cfg"


def _get_string_from_config(
    config: ConfigParser, section: str, option: str
) -> Optional[str]:
    # Try to get the value from the config
    try:
        str_with_quotes = config.get(section, option)
    except (KeyError, AttributeError):
        return None
    else:
        # Remove the quotes from the string, but only if they exist
        if str_with_quotes.startswith('"') and str_with_quotes.endswith('"'):
            return str_with_quotes[1:-1]
        elif str_with_quotes.startswith("'") and str_with_quotes.endswith("'"):
            return str_with_quotes[1:-1]
        else:
            return str_with_quotes
