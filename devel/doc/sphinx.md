# sphinx

<https://www.sphinx-doc.org/>

Sphinx makes it easy to create intelligent and beautiful documentation.

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

If your `python3` is installed by `brew`, try:

```sh
pip3 install -r requirements.txt --break-system-packages
```

Check the version:

```sh
sphinx-build --version
```

{.cli-output}

```text
sphinx-build 7.3.7
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
:language: python
:diff: /conf.py.orig
:class: file-content
:::

Build html:

```sh
make html
```

Thne open `_build/html/index.html` in your browser.
