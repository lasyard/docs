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

First, download the binary package:

```sh
wget https://cmake.org/files/v3.27/cmake-3.27.7-linux-x86_64.tar.gz
```

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

Download the sources:

```sh
wget https://cmake.org/files/v3.27/cmake-3.27.7.tar.gz
```

::::{plat} centos
:vers: CentOS 8.5

:::{include} /_files/frags/toolchain/centos_gcc_11.txt
:::

Install some dependencies:

```sh
sudo dnf install openssl-devel
```

Extract the sources:

```sh
tar -C ~/workspace/devel -xzf cmake-3.27.7.tar.gz
cd ~/workspace/devel/cmake-3.27.7/
```

Build and install it:

```sh
./bootstrap
make
sudo make install
```

::::
