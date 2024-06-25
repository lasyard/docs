# cmake

<https://cmake.org/>

CMake: A Powerful Software Build System

CMake is the de-facto standard for building C++ code, with over 2 million downloads a month. It’s a powerful, comprehensive solution for managing the software build process. Get everything you need to successfully leverage CMake by visiting our resources section.

## Install

{{ for_macos }}

```sh
brew install cmake
```

```sh
cmake --version
```

{.cli-output}

```text
cmake version 3.29.6

CMake suite maintained and supported by Kitware (kitware.com/cmake).
```

{{ for_centos }}

```sh
dnf install cmake
```

This version is quite old, so you may want ot install a newer version manually.

First, download the latest binary distribution from <https://cmake.org/download/>.

Uncompress it:

```sh
tar -C /usr/local --strip-components=1 -xzvf cmake-3.27.7-linux-x86_64.tar.gz
```

```sh
cmake --version
```

{.cli-output}

```text
cmake version 3.27.7

CMake suite maintained and supported by Kitware (kitware.com/cmake).
```

## Build from sources

{{ for_centos }}

{{ centos_build }}

You can also download the source, then build and install it:

```sh
tar -xzf cmake-3.27.7.tar.gz
cd cmake-3.27.7/
./bootstrap
make
make install
```
