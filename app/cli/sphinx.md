# Sphinx

<https://www.sphinx-doc.org/>

## Prerequisites

Install `python3` and `pip3`, see <project:/devel/python/install.md>.

## Install

Edit file `requirements.txt`:

:::{literalinclude} /requirements.txt
:::

Install the requirements:

```console
$ pip3 install -r requirements.txt
```

Check the version:

```console
$ sphinx-build --version
sphinx-build 8.1.3
```

## Usage

In your working directory:

```console
$ sphinx-quickstart
```

Edit file `conf.py`:

:::{literalinclude} /conf.py
:diff: /conf.py.orig
:::

Build html:

```console
$ make html
```

Then open `_build/html/index.html` in your browser.

### Build pdf

Need `latexmk`. On macOS, install BasicTex from <https://www.tug.org/mactex/morepackages.html>. Then install `latexmk`:

```console
$ sudo tlmgr update --self
$ sudo tlmgr install latexmk
```

```console
$ latexmk --version
Latexmk, John Collins, 9 March 2026. Version 4.88
```

Common packages may be needed:

```console
$ sudo tlmgr install tex-gyre collection-fontsrecommended collection-latexrecommended collection-fontsextra
```

More:

```console
sudo tlmgr install fncychap tabulary capt-of framed needspace wrapfig multirow varwidth cmap upquote parskip titlesec eqparbox environ trimspaces mdframed zref etoolbox tocloft xcolor float wrapfig ucs pict2e ellipse
```

For CJK characters:

```console
$ sudo tlmgr install xecjk fandol
```

In your `conf.py`:

```py
latex_engine = 'xelatex'
latex_elements = {
    'preamble': r'''
\usepackage{xeCJK}
\setCJKmainfont{Source Han Serif CN VF} # 思源宋体
''',
}
```

Need `mmdc` to convert mermaid graph:

```console
$ PUPPETEER_SKIP_DOWNLOAD=true npm install -g --allow-scripts=puppeteer @mermaid-js/mermaid-cli
```

Set `PUPPETEER_SKIP_DOWNLOAD=true` to skip downloading Chromium for we can use the existing Chrome (if there is). Need a config file:

:::{literalinclude} /_files/macos/home/config/puppeteer-config.json
:::

Put the file to `~/.config/puppeteer-config.json`. Set `mmdc` command in `conf.py`:

```py
mermaid_cmd = "/Users/jyg/.nvm/versions/node/v24.18.0/bin/mmdc"
mermaid_params = ["-p", "/Users/jyg/puppeteer-config.json"]
```
