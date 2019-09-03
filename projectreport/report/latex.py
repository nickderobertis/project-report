import pyexlatex as pl
from pyexlatex.models.section.base import TextAreaMixin
from pyexlatex.models.item import ItemBase
from pyexlatex.models.format.breaks import OutputLineBreak
from pyexlatex.models.format.adjustwidth import AdjustWidth


class SubProjectLatex(TextAreaMixin, ItemBase):

    def __init__(self, data, **kwargs):
        contents = self.get_contents(data)
        super().__init__(None, contents, **kwargs)

    def get_contents(self, data):
        line_break = OutputLineBreak()
        contents = [
            pl.Bold(data['name']) if data['name'] else None,
            pl.TextColor(f"{data['lines']} LOC", color='green') if data['lines'] else None,
            f'created {data["created"]}' if data["created"] else None,
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


def project_latex(data):
    contents = []
    contents.append(SubProjectLatex(data))
    if 'subprojects' in data:
        for project in data['subprojects']:
            contents.append(AdjustWidth(project_latex(data['subprojects'][project])))
    return contents


def project_latex_document(data) -> pl.Document:
    contents = project_latex(data)
    return pl.Document(contents)
