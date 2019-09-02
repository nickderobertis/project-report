from typing import Optional, List, Sequence, TYPE_CHECKING
if TYPE_CHECKING:
    from projectreport.analyzer.module import Module
import pygount


class FolderAnalysis:

    def __init__(self):
        self.lines = {key: 0 for key in [
            'code',
            'documentation',
            'empty',
            'string'
        ]}

    def __repr__(self):
        return f'<PackageAnalysis(lines={self.lines})>'

    def add_module_analysis(self, analysis: 'ModuleAnalysis'):
        for attr in self.lines:
            value = getattr(analysis.source_analysis, attr)
            if value is None:
                value = 0
            self.lines[attr] += value

    def add_subfolder_analysis(self, analysis: 'FolderAnalysis'):
        for attr in self.lines:
            value = analysis.lines[attr]
            if value is None:
                value = 0
            self.lines[attr] += value


class ModuleAnalysis:

    def __init__(self, module: 'Module'):
        self.module = module
        self.source_analysis = pygount.source_analysis(self.module.path, self.module.package)
        self.git_analysis = GitAnalysis(self.module)


class GitAnalysis:

    def __init__(self, module: 'Module'):
        self.module = module
        self.num_commits = module.num_commits

