"""
A set of tools for describing software projects. Finds software projects, analyzes them,
and outputs reports.
"""
from projectreport.analyzer.project import Project
from projectreport.finder.python import PythonPackageFinder
from projectreport.finder.git import GitFinder
from projectreport.finder.combine import CombinedFinder
from projectreport.report.report import Report
from projectreport.config import DEFAULT_IGNORE_PATHS
from projectreport.analyzer.ts.github import GithubAnalysis
