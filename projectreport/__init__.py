"""
A set of tools for describing software projects. Finds software projects, analyzes them,
and outputs reports.
"""
from projectreport.analyzer.project import Project
from projectreport.analyzer.ts.github import GithubAnalysis
from projectreport.config import DEFAULT_IGNORE_PATHS
from projectreport.finder.combine import CombinedFinder
from projectreport.finder.git import GitFinder
from projectreport.finder.js import JavaScriptPackageFinder
from projectreport.finder.python import PythonPackageFinder
from projectreport.report.report import Report
