# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

from datetime import date


sys.path.append(os.path.abspath("./_ext"))

project = "Lasy's Documentation"
copyright = '%Y, Lasy'
author = 'Lasy'
release = 'latest'
language = 'en'
html_logo = '_images/lasydoc.png'
html_favicon = '_images/favicon-96x96.png'


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'myst_parser',
    'sphinx_copybutton',
    'sphinx_rtd_theme',
    'sphinx_tabs.tabs',
    'sphinxcontrib.mermaid',
]

extensions += [
    'ellipsis_to_vertical',
]

copybutton_prompt_is_regexp = True
copybutton_prompt_text = r"^\$ |^# |^% "

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
exclude_patterns = ['.*', '_*', 'Thumbs.db', 'README.*']

myst_substitutions = {
}


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

if html_theme == 'sphinx_rtd_theme':
    html_css_files = ['css/lasy_sphinx_rtd_theme.css']


# https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#auto-generated-header-anchors

myst_heading_anchors = 3
