import pygount


class PackageAnalysis:

    def __init__(self):
        self.lines = {key: 0 for key in [
            'code',
            'documentation',
            'empty',
            'string'
        ]}

    def __repr__(self):
        return f'<PackageAnalysis(lines={self.lines})>'

    def add_module_analysis(self, analysis: pygount.SourceAnalysis):
        for attr in self.lines:
            value = getattr(analysis, attr)
            if value is None:
                value = 0
            self.lines[attr] += value

    def add_subpackage_analysis(self, analysis: 'PackageAnalysis'):
        for attr in self.lines:
            value = analysis.lines[attr]
            if value is None:
                value = 0
            self.lines[attr] += value
