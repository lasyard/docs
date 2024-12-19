# cmake

<https://cmake.org/>

## Install

### By package mangager

::::{plat} macos
:vers: macOS Monterey

```sh
brew install cmake
```

Check the version:

:::{literalinclude} /_files/macos/console/cmake/version.txt
:language: console
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

Check the version:

:::{literalinclude} /_files/centos/console/cmake/version.txt
:language: console
:::

::::

### Build from sources

::::{plat} centos
:vers: CentOS 8.5

:::{include} /_files/frags/toolchain/centos_gcc_11.txt
:::

Download the source, then build and install it:

```sh
tar -xzf cmake-3.27.7.tar.gz
cd cmake-3.27.7/
./bootstrap
make
sudo make install
```

::::
