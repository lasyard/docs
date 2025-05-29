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
