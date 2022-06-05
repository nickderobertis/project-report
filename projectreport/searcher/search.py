import os
import re
from pathlib import Path
from typing import (
    Dict,
    Generator,
    Iterator,
    List,
    Optional,
    Sequence,
    Set,
    Tuple,
    Union,
)

from projectreport.searcher.rotating_list import RotatingList
from projectreport.tools.expand_glob import all_possible_paths


def read_all_files_in_folders_print_lines_around_regex(
    folders: Sequence[str],
    str_pattern: str,
    num_lines: int = 2,
    recursive: bool = False,
    print_lines: bool = True,
    ignore_paths: Optional[Sequence[str]] = None,
) -> Dict[str, List[List[str]]]:
    """
    Searches for regex in each line of every file in multiple folders. When regex is
    matched, will return num_lines lines around the file

    :param folders: Folders to search in
    :param str_pattern: Pattern to match in a line
    :param num_lines: Number of lines around the matching line to return/print,
        defaults to 2
    :param recursive: Whether to search folders within passed folder, defaults to False
    :param print_lines: Whether to print the results, defaults to False
    :param ignore_paths: Relative paths to ignore. Globs are accepted, defaults to None
    :return: a dictionary where keys are file paths, and values are lists where each
        element is a list containing the lines for one match
    """
    found_lines = {}
    for folder in folders:
        found_lines.update(
            read_all_files_in_folder_print_lines_around_regex(
                folder,
                str_pattern,
                num_lines=num_lines,
                recursive=recursive,
                print_lines=print_lines,
                ignore_paths=ignore_paths,
            )
        )
    return found_lines


def read_all_files_in_folder_print_lines_around_regex(
    file_path: str,
    str_pattern: str,
    num_lines: int = 2,
    recursive: bool = False,
    print_lines: bool = True,
    ignore_paths: Optional[Sequence[str]] = None,
) -> Dict[str, List[List[str]]]:
    """
    Searches for regex in each line of every file in a folder. When regex is matched,
    will return num_lines lines around the file

    :param file_path: Path of file to search in
    :param str_pattern: Pattern to match in a line
    :param num_lines: Number of lines around the matching line to return/print,
        defaults to 2
    :param recursive: Whether to search folders within passed folder, defaults to False
    :param print_lines: Whether to print the results, defaults to False
    :param ignore_paths: Relative paths to ignore. Globs are accepted, defaults to None
    :return: a dictionary where keys are file paths, and values are lists where each
        element is a list containing the lines for one match
    """

    iterator: Union[
        List[Tuple[str, List[str], List[str]]],
        Iterator[Tuple[str, List[str], List[str]]],
    ]
    if recursive:
        iterator = os.walk(file_path)
    else:
        iterator = [next(os.walk(file_path))]

    if ignore_paths is None:
        ignore_paths = []

    all_absolute_ignore_paths: Set[Path] = set()
    found_lines = {}

    def should_ignore_path(path_str: str) -> bool:
        path = Path(path_str)
        for ignore_path in all_absolute_ignore_paths:
            if path == ignore_path or ignore_path in path.parents:
                return True
        return False

    for path, folders, files in iterator:
        expanded_ignore_paths = all_possible_paths(ignore_paths, path)
        all_absolute_ignore_paths.update(
            set([Path(path_str) for path_str in expanded_ignore_paths])
        )
        if should_ignore_path(path):
            # Skip ignored folder
            continue
        for file in files:
            full_path = os.path.join(path, file)
            if should_ignore_path(full_path):
                # Skip ignored file
                continue
            lines = read_file_get_lines_around_regex(
                full_path, str_pattern, num_lines=num_lines, print_lines=False
            )
            if lines:
                found_lines[full_path] = lines
                if print_lines:
                    print(f"\n\nFound {len(lines)} match in {full_path}")
                    for line_set in lines:
                        _print_tracked_lines(line_set)

    return found_lines


def read_file_get_lines_around_regex(
    file_path: str, str_pattern: str, num_lines: int = 2, print_lines: bool = False
) -> List[List[str]]:
    """
    Searches for regex in each line of a file. When regex is matched, will return
    num_lines lines around the file

    :param file_path: path of file to search in
    :param str_pattern: pattern to match in a line
    :param num_lines: number of lines around the matching line to return/print,
        defaults to 2
    :param print_lines: whether to print the results, defaults to False
    :return: a list where each element is a list containing the lines for one match
    """
    reader = _file_reader(file_path)
    lines = _get_lines_around_regex(
        str_pattern, reader, num_lines=num_lines, print_lines=print_lines
    )
    return lines


def _file_reader(filename):
    try:
        with open(filename, "r", encoding="utf8") as f:
            for line in f:
                yield line.strip()
    except UnicodeDecodeError:
        try:
            with open(filename, "r", encoding="latin1") as f:
                for line in f:
                    yield line.strip()
        except Exception as e:
            print(f"Could not read file {filename}: {e}")
            return


def _get_lines_around_regex(
    str_pattern: str,
    lines: Generator[str, None, None],
    num_lines: int = 2,
    print_lines: bool = False,
) -> List[List[str]]:
    pattern = re.compile(str_pattern)

    total_num_lines = (
        num_lines * 2 + 1
    )  # 1 line for match, then 2 * num_lines for before and after match

    # After finding a match, must delay the print for num_lines as only
    # then will we have the lines after
    # the match. Set up this list to track at which lines we should print
    print_at_lines = []

    # Keeps only the last total_num_lines entires
    tracked_lines = RotatingList([], total_num_lines)

    # Will hold each set of found lines to return at the end
    found_lines = []

    def record_lines():
        found_lines.append(list(tracked_lines))
        if print_lines:
            _print_tracked_lines(tracked_lines)

    # Find and track lines which have matches, printing num_lines after
    for i, line in enumerate(lines):
        line_num = i + 1
        tracked_lines.append(f"{line_num}: {line}")
        if _matches_regex(pattern, line):
            print_at_lines.append(line_num + num_lines)
        if line_num in print_at_lines:
            record_lines()

    # Print final section if requested line to print at was after the end of the file
    if any([print_line_num > line_num for print_line_num in print_at_lines]):
        record_lines()

    return found_lines


def _print_tracked_lines(lines: Union[RotatingList, List[str]]) -> None:
    print("\n" + "\n".join(lines))


def _matches_regex(pattern: re.Pattern, search_str: str) -> bool:
    match = re.search(pattern, search_str)
    return match is not None
