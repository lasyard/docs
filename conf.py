# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

from datetime import date


project = "Lasy's Documentation"
copyright = date.today().strftime('%Y') + ', Lasy'
author = 'Lasy'
release = 'latest'
language = 'en'


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'myst_parser',
    'sphinx_copybutton',
    'sphinx_prompt', # not working well with sphinx_copybutton
    'sphinx_rtd_theme',
    'sphinxcontrib.mermaid',
]

myst_enable_extensions = [
    'attrs_block',
    'attrs_inline',
    'colon_fence',
    'deflist',
    'fieldlist',
    'substitution',
    'tasklist',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', 'README.md']


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']


# https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#auto-generated-header-anchors

myst_heading_anchors = 3
