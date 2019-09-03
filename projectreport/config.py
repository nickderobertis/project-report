import os

DEFAULT_IGNORE_PATHS = (
    os.path.sep.join(['**', '.*']),  # hidden files and folders
    os.path.sep.join(['**', '__pycache__']),  # python cache
)
