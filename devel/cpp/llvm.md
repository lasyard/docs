# LLVM

<https://llvm.org/>

## Install

::::{plat} macos
:vers: macOS Monterey

```sh
brew install llvm
```

`clang` is already installed as part of "Xcode Command Line Tools" on this version of macOS. Before install `llvm`:

:::{literalinclude} /_files/macos/console/clang/v.txt
:language: console
:::

After install `llvm`:

:::{literalinclude} /_files/macos/console/clang/v_18.txt
:language: console
:::

:::{note}
Environment variables must set for the build system (such as CMake) to detect the compiler:

```sh
export CC=clang
export CXX=clang++
export CFLAGS=-I/usr/local/opt/llvm/include
export CPPFLAGS=-I/usr/local/opt/llvm/include
export CXXFLAGS=-I/usr/local/opt/llvm/include
export LDFLAGS=-L/usr/local/opt/llvm/lib
```

:::

:::{tip}
You may need to add these paths if Xcode Command Line Tools was installed:

- header path: `$(xcode-select -p)/SDKs/MacOSX.sdk/usr/include`
- lib path: `$(xcode-select -p)/SDKs/MacOSX.sdk/usr/lib`

:::

::::
