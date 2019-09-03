from typing import List
import pyexlatex as pl
from pyexlatex.models.section.base import TextAreaMixin
from pyexlatex.models.item import ItemBase
from pyexlatex.models.format.breaks import OutputLineBreak


class SubProjectLatex(TextAreaMixin, ItemBase):

    def __init__(self, data, **kwargs):
        contents = self.get_contents(data)
        super().__init__(None, contents, **kwargs)

    def get_contents(self, data):
        line_break = OutputLineBreak()
        green = pl.RGB(42, 138, 11, color_name='darkgreen')
        commits_str = 'Commits' if data['num_commits'] and data['num_commits'] > 1 else 'Commit'
        contents = [
            pl.Bold(data['name']) if data['name'] else None,
            pl.TextColor(f"{data['lines']} LOC", color=green) if data['lines'] else None,
            ['|', pl.TextColor(f"{data['num_commits']} {commits_str}", color='blue')] if data['num_commits'] else None,
            ['|', f'Created {data["created"].date()}'] if data["created"] else None,
            ['|', f'Updated {data["updated"].date()}'] if data["updated"] else None,
            line_break,
            data['docstring'],
        ]
        contents = [content for content in contents if content is not None]
        if not contents[-1] == line_break:
            contents.append(line_break)
        return contents

    def __str__(self):
        from pyexlatex.logic.builder import _build
        if isinstance(self.contents, str):
            return self.contents
        return _build(self.contents)


def project_latex(data: dict):
    contents = []
    contents.append(SubProjectLatex(data))
    if 'subprojects' in data:
        for project in data['subprojects']:
            contents.append(pl.ParagraphIndent(project_latex(data['subprojects'][project])))
    return contents


def multi_project_latex(data: List[dict]):
    contents = []
    for data_dict in data:
        contents.extend([
            project_latex(data_dict),
            pl.HLine(),
            pl.VSpace(0.5),
        ])

    del contents[-2:]  # remove last horizontal line and vertical spacing
    return contents


def project_latex_document(data) -> pl.Document:
    contents = project_latex(data)
    return _get_document(contents)


def multi_project_latex_document(data: List[dict]) -> pl.Document:
    contents = multi_project_latex(data)
    return _get_document(contents)


def _get_document(contents) -> pl.Document:
    doc = pl.Document(
        contents,
        title='Project Report'
    )
    return doc
