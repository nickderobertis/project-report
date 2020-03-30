"""
This is a patch for the bug:

File "/home/nick/.local/share/virtualenvs/project-report-PocZQ6Fg/lib/python3.7/site-packages/sphinx/domains/python.py", line 1145, in clear_doc
    for fullname, (fn, _x, _x) in list(self.objects.items()):
ValueError: not enough values to unpack (expected 3, got 2)

Debugging:
(Pdb) len(list(self.objects.items())
*** SyntaxError: unexpected EOF while parsing
(Pdb) len(list(self.objects.items()))
158
(Pdb) items = list(self.objects.items())
(Pdb) len([item for item in items if len(item[1]) != 3])
32
(Pdb) bad_items = [item for item in items if len(item[1]) != 3]
(Pdb) good_items = [item for item in items if len(item[1]) == 3]
(Pdb) good_items[0]
('projectreport', ('api/projectreport', 'module-projectreport', 'module'))
(Pdb) good_items[1]
('projectreport.config', ('api/projectreport', 'module-projectreport.config', 'module'))
(Pdb) bad_items[0]
('projectreport.searcher.read_all_files_in_folder_print_lines_around_regex.params.file_path', ('api/projectreport.searcher', 'parameter'))
(Pdb) bad_items[1]
('projectreport.searcher.read_all_files_in_folder_print_lines_around_regex.params.str_pattern', ('api/projectreport.searcher', 'parameter'))
(Pdb) len([item for item in good_items if item[1][2] == 'parameter'])
0
(Pdb) len([item for item in bad_items if item[1][2] == 'parameter'])
*** IndexError: tuple index out of range
(Pdb) len([item for item in bad_items if item[1][1] == 'parameter'])
32
(Pdb) len([item for item in good_items if item[1][1] == 'parameter'])
0
(Pdb) docname
'api/projectreport.tools'

To patch that issue, I applied the clear_doc patch below. Then was facing another issue:

Exception occurred:
  File "/home/nick/.local/share/virtualenvs/project-report-PocZQ6Fg/lib/python3.7/site-packages/sphinx/domains/python.py", line 1278, in get_objects
    for refname, (docname, node_id, type) in self.objects.items():
ValueError: not enough values to unpack (expected 3, got 2)

In debugging, I found the same objects were coming to get_objects, and because of that it was facing a similar issue.

To patch that issue, I applied the get_objects patch below to skip the objects which have the wrong number of items

This may be fixed in version 3.1.0 because of the restructure in https://github.com/sphinx-doc/sphinx/pull/7363
"""
from typing import Iterator, Tuple

from sphinx.domains.python import PythonDomain


class PatchedPythonDomain(PythonDomain):

    def clear_doc(self, docname: str) -> None:
        for fullname, obj_tup in list(self.objects.items()):
            fn = obj_tup[0]
            if fn == docname:
                del self.objects[fullname]
        for modname, (fn, _x, _x, _x, _y) in list(self.modules.items()):
            if fn == docname:
                del self.modules[modname]

    def get_objects(self) -> Iterator[Tuple[str, str, str, str, str, int]]:
        for modname, info in self.modules.items():
            yield (modname, modname, 'module', info[0], info[1], 0)
        for refname, obj_tup in self.objects.items():
            try:
                (docname, node_id, type) = obj_tup
            except ValueError as e:
                if 'not enough values to unpack' in str(e):
                    continue
            if type != 'module':  # modules are already handled
                yield (refname, refname, type, docname, node_id, 1)