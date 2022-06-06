from enum import Enum


class ParserDataType(str, Enum):
    SINGLE_FILE = "single_file"
    FOLDER = "folder"
    URL = "url"
