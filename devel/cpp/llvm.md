# LLVM

<https://llvm.org/>

The LLVM Project is a collection of modular and reusable compiler and toolchain technologies. Despite its name, LLVM has little to do with traditional virtual machines. The name "LLVM" itself is not an acronym; it is the full name of the project.

## Install

::::{plat} macos
:vers: macOS Monterey

```sh
brew install llvm
```

:::{note}
`clang` is already installed by default on this version of macOS. This new version will replace it. To show the `clang` version, run:

```sh
clang --version
```

The output for the system `clang`:

:::{literalinclude} /_files/macos/output/clang/version.txt
:language: text
:class: cli-output
:::

The output for the Homebrew installed `clang`:

:::{literalinclude} /_files/macos/output/clang/version_1.txt
:language: text
:class: cli-output
:::

::::
