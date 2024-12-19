# clang-format

## Install

::::{plat} macos
:vers: macOS Monterey

`clang-format` is installed along with `llvm`, see <project:llvm.md>.

Check the version:

```console
$ type clang-format
clang-format is /usr/local/opt/llvm/bin/clang-format
$ clang-format --version
Homebrew clang-format version 18.1.8
```

::::

## Usage

Format all c/cpp code in the current directory, excluding doctest files:

```sh
find . -not -path '*/doctest/*' \( -name '*.cpp' -or -name '*.c' -or -name '*.h' \) -exec clang-format -i {} \;
```
