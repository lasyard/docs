# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sys

from pathlib import Path

sys.path.append(str(Path('sphinx-common/ext').resolve()))

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
    'sphinx_design',
    'sphinx_rtd_theme',
    'sphinxcontrib.mermaid',
]

extensions += [
    'lasyard_literalinclude',
    'ellipsis_to_vertical',
]

copybutton_prompt_is_regexp = True
copybutton_prompt_text = r"^\$ |^# |^% "

myst_enable_extensions = [
    'attrs_block',
    'attrs_inline',
    'colon_fence',
    'deflist',
    'dollarmath',
    'fieldlist',
    'substitution',
    'tasklist',
]

myst_dmath_allow_labels=True

templates_path = ['_templates']
exclude_patterns = ['.*', '_*', 'Thumbs.db', 'README.*']
exclude_patterns += ['sphinx-common']

myst_substitutions = {
}


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['sphinx-common/static']

if html_theme == 'sphinx_rtd_theme':
    html_css_files = ['lasyard_sphinx_rtd_theme.css']

# https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#auto-generated-header-anchors

myst_heading_anchors = 3
