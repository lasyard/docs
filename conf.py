# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sys

sys.path.append('.')

from lasphinx import *

project = "Lasy's Documentation"
copyright = '%Y, Lasy'
author = 'Lasy'
release = 'latest'
language = 'en'
html_logo = '_images/lasydoc.png'
html_favicon = '_images/favicon-96x96.png'

myst_substitutions = {
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'

if html_theme == 'sphinx_rtd_theme':
    html_css_files = ['lasyard_sphinx_rtd_theme.css']
