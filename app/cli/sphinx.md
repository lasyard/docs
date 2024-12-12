# Sphinx

<https://www.sphinx-doc.org/>

## Prerequisites

Install `python3` and `pip3`.

## Install

```sh
vi requirements.txt
```

:::{literalinclude} /requirements.txt
:language: text
:class: file-content
:::

```sh
pip3 install -r requirements.txt
```

Check the version:

```console
$ sphinx-build --version
sphinx-build 8.1.3
```

## Usage

In your working directory:

```sh
sphinx-quickstart
```

```sh
vi conf.py
```

:::{literalinclude} /conf.py
:diff: /conf.py.orig
:class: file-content
:::

Build html:

```sh
make html
```

Then open `_build/html/index.html` in your browser.
