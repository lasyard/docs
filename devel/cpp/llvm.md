# LLVM

<https://llvm.org/>

## Install

:::::{tab-set}
::::{tab-item} macOS Monterey

```console
$ brew install llvm
```

`clang` is already installed as part of "Xcode Command Line Tools" on this version of macOS. Show the versions:

```console
$ /usr/bin/clang -v
Apple clang version 14.0.0 (clang-1400.0.29.202)
Target: x86_64-apple-darwin21.6.0
Thread model: posix
InstalledDir: /Library/Developer/CommandLineTools/usr/bin
$ /usr/local/opt/llvm/bin/clang -v
Homebrew clang version 18.1.8
Target: x86_64-apple-darwin21.6.0
Thread model: posix
InstalledDir: /usr/local/opt/llvm/bin
```

:::{note}
Environment variables must set for the build system (such as CMake) to detect the compiler:

```sh
export PATH=/usr/local/opt/llvm/bin:${PATH}
export CC=clang
export CXX=clang++
```

:::

::::
:::::

## clang-format

`clang-format` is installed along with `LLVM`, check the version:

```console
$ clang-format --version
Homebrew clang-format version 18.1.8
```

Format all c/cpp code in the current directory, excluding `doctest` files:

```console
$ find . -not -path '*/doctest/*' \( -name '*.cpp' -or -name '*.c' -or -name '*.h' \) -exec clang-format -i {} \;
```
