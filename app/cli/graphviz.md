# graphviz

<https://graphviz.org/>

## Install

::::{tab-set}
:::{tab-item} macOS
:sync: macos

```console
$ brew install graphviz
```

:::
::::

Check the version:

```console
$ dot -V
dot - graphviz version 12.1.0 (20240811.2233)
```

## Usage

Generate svg:

```console
$ dot -Tsvg input.dot
```
