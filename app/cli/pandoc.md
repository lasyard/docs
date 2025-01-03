# pandoc

<https://pandoc.org/>

## Install

::::{plat} macos
:vers: macOS Monterey

```sh
brew install pandoc
```

:::{literalinclude} /_files/macos/console/pandoc/version.txt
:language: console
:::

::::

## Usage

Convert `docx` to `md`:

```sh
pandoc xxxx.docx -f docx -t markdown -o xxxx.md
```
