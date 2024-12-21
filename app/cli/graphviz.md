# graphviz

<https://graphviz.org/>

## Install

::::{plat} macos
:vers: macOS Monterey

```sh
brew install graphviz
```

Check the version:

```console
$ dot -V
dot - graphviz version 12.1.0 (20240811.2233)
```

::::

## Usage

Generate svg:

```sh
dot -Tsvg input.dot
```
