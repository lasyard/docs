# cmake

<https://cmake.org/>

CMake: A Powerful Software Build System

CMake is the de-facto standard for building C++ code, with over 2 million downloads a month. It’s a powerful, comprehensive solution for managing the software build process. Get everything you need to successfully leverage CMake by visiting our resources section.

## Install

### By package mangager

::::{plat} macos
:vers: macOS Monterey

```sh
brew install cmake
```

```sh
cmake --version
```

:::{literalinclude} /_files/macos/output/cmake/version.txt
:language: text
:class: cli-output
:::

::::

::::{plat} centos
:vers: CentOS 8.5

```sh
sudo dnf install cmake
```

This version is quite old, so you may want ot install a newer version manually.
::::

### Manually install from a release tarball

::::{plat} linux
:vers: CentOS 8.5

First, download the latest binary distribution from <https://cmake.org/download/>.

Uncompress it:

```sh
sudo tar -C /usr/local --strip-components=1 -xzvf cmake-3.27.7-linux-x86_64.tar.gz
```

```sh
cmake --version
```

:::{literalinclude} /_files/centos/output/cmake/version.txt
:language: text
:class: cli-output
:::

::::

### Build from sources

::::{plat} centos
:vers: CentOS 8.5

The toolchain used:

- gcc 11.2.1
- GNU Make 4.3

Download the source, then build and install it:

```sh
tar -xzf cmake-3.27.7.tar.gz
cd cmake-3.27.7/
./bootstrap
make
sudo make install
```

::::
