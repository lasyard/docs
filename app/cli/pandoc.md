# pandoc

<https://pandoc.org/>

## Install

::::{tab-set}
:::{tab-item} macOS Monterey

```console
$ brew install pandoc
```

Check the version:

```console
$ pandoc --version
pandoc 3.3
Features: +server +lua
Scripting engine: Lua 5.4
User data directory: /Users/xxxx/.local/share/pandoc
Copyright (C) 2006-2024 John MacFarlane. Web: https://pandoc.org
This is free software; see the source for copying conditions. There is no
warranty, not even for merchantability or fitness for a particular purpose.
```

:::
::::

## Usage

Convert `docx` to `md`:

```console
pandoc xxxx.docx -f docx -t markdown -o xxxx.md
```
