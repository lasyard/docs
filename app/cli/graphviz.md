# graphviz

<https://graphviz.org/>

Graphviz is open source graph visualization software. Graph visualization is a way of representing structural information as diagrams of abstract graphs and networks.

## Install

::::{plat} macos
:vers: macOS Monterey

```sh
brew install graphviz
```

See version:

```sh
dot -V
```

{.cli-output}

```text
dot - graphviz version 11.0.0 (20240428.1522)
```

::::

## Usage

Generate svg:

```sh
dot -Tsvg input.dot
```
