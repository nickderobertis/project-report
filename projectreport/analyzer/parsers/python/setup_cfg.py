import ast
import configparser
from configparser import ConfigParser, ParsingError
from pathlib import Path
from typing import List, Optional, Union

from cached_property import cached_property

from projectreport.analyzer.parsers.base import Parser
from projectreport.analyzer.parsers.python.base import PythonParser
from projectreport.analyzer.parsers.python.classifier_topics import (
    get_topics_from_classifiers,
    get_topics_from_classifiers_str,
)
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

    @cached_property
    def topics(self) -> Optional[List[str]]:
        if self.parsed is None:
            return None

        classifiers = _get_from_config(self.parsed, "metadata", "classifiers")
        if classifiers is None:
            return None
        topics = get_topics_from_classifiers_str(classifiers)
        return topics

    @classmethod
    def matches_path(cls, path: str) -> bool:
        return Path(path).name == "setup.cfg"


def _get_from_config(config: ConfigParser, section: str, option: str) -> Optional[str]:
    # Try to get the value from the config
    try:
        return config.get(section, option)
    except (
        KeyError,
        AttributeError,
        configparser.NoOptionError,
        configparser.NoSectionError,
    ):
        return None


def _get_string_from_config(
    config: ConfigParser, section: str, option: str
) -> Optional[str]:
    # Try to get the value from the config
    str_with_quotes = _get_from_config(config, section, option)
    if str_with_quotes is None:
        return None

    # Remove the quotes from the string, but only if they exist
    if str_with_quotes.startswith('"') and str_with_quotes.endswith('"'):
        return str_with_quotes[1:-1]
    elif str_with_quotes.startswith("'") and str_with_quotes.endswith("'"):
        return str_with_quotes[1:-1]
    else:
        return str_with_quotes
