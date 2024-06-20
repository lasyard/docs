# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

from datetime import date


project = 'Lasy Documentation'
copyright = date.today().strftime('%Y') + ', Lasy'
author = 'Lasy'
release = 'latest'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'myst_parser',
    'sphinxcontrib.mermaid',
    'sphinx_rtd_theme',
    # not working well with sphinx_copybutton
    # 'sphinx_prompt',
    'sphinx_copybutton',
]

myst_enable_extensions = [
    'colon_fence',
    'deflist',
    'fieldlist',
    'tasklist',
    'attrs_inline',
    'attrs_block',
    'substitution',
]

myst_substitutions = {
    'for_macos': ":::{include} /_frags/for/macos.txt\n:::",
    'for_centos': ":::{include} /_frags/for/centos.txt\n:::",
    'for_ubuntu': ":::{include} /_frags/for/ubuntu.txt\n:::",
    'for_win10': ":::{include} /_frags/for/win10.txt\n:::",
    'macos_build': ":::{include} /_frags/build/macos.txt\n:::",
    'centos_build': ":::{include} /_frags/build/centos.txt\n:::",
    'ubuntu_build': ":::{include} /_frags/build/ubuntu.txt\n:::",
    'cluster_las': ":::{include} /_frags/cluster/las.txt\n:::",
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', 'README.*']

language = 'en'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

if html_theme == 'sphinx_rtd_theme':
    html_css_files = ['css/lasy_sphinx_rtd_theme.css']

# https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#auto-generated-header-anchors
myst_heading_anchors = 3
