# clang-format

## Install

::::{plat} macos
:vers: macOS Monterey

```sh
brew install clang-format
```

```sh
clang-format --version
```

{.cli-output}

```text
clang-format version 18.1.7
```

::::

## Usage

Format all c/cpp code in the current directory, excluding doctest files:

```sh
find . -not -path '*/doctest/*' \( -name '*.cpp' -or -name '*.c' -or -name '*.h' \) -exec clang-format -i {} \;
```
