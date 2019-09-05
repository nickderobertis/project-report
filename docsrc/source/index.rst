.. pypi-sphinx-quickstart documentation master file, created by
   pypi-sphinx-quickstart.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Project Report documentation!
*********************************************

To get started, look here.

.. toctree::

   tutorial


An overview
============

Finder
----------

.. autosummary::

      projectreport.finder.base.Finder
      projectreport.finder.git.GitFinder
      projectreport.finder.python.PythonPackageFinder
      projectreport.finder.combine.CombinedFinder

Project
----------------

.. autosummary::

      projectreport.analyzer.project.Project

Report
----------------

.. autosummary::

      projectreport.report.report.Report

API Documentation
------------------

A full list of modules

.. toctree:: api/modules
   :maxdepth: 3

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
