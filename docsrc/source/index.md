% pypi-sphinx-quickstart documentation master file, created by
% pypi-sphinx-quickstart.
% You can adapt this file completely to your liking, but it should at least
% contain the root `toctree` directive.

# Welcome to Project Report documentation!

To get started, look here.

```{toctree}
tutorial
```

## An overview

### Finder

```{eval-rst}
.. autosummary::

      projectreport.finder.base.Finder
      projectreport.finder.git.GitFinder
      projectreport.finder.python.PythonPackageFinder
      projectreport.finder.combine.CombinedFinder
```

### Project

```{eval-rst}
.. autosummary::

      projectreport.analyzer.project.Project
```

### Report

```{eval-rst}
.. autosummary::

      projectreport.report.report.Report
```

### API Documentation

A full list of modules

```{toctree}
:maxdepth: 3

api/modules
```

## Indices and tables

- {ref}`genindex`
- {ref}`modindex`
- {ref}`search`
