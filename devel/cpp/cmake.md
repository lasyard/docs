# Install CMake

<https://cmake.org/>

## By package manager

::::{tab-set}
:::{tab-item} macOS Monterey

```console
$ brew install cmake
```

Check the version:

```console
$ cmake --version
cmake version 3.30.3

CMake suite maintained and supported by Kitware (kitware.com/cmake).
```

:::
:::{tab-item} CentOS 8.5

```console
$ sudo dnf install cmake
```

This version is quite old, so you may want ot install a newer version manually.

:::
::::

## From a release tarball

First, download the binary package:

```console
$ curl -LO https://cmake.org/files/v3.27/cmake-3.27.7-linux-x86_64.tar.gz
```

Uncompress it:

```console
$ sudo tar -C /usr/local --strip-components=1 -xzvf cmake-3.27.7-linux-x86_64.tar.gz
```

It is OK now. Check the version:

```console
$ cmake --version
cmake version 3.27.7

CMake suite maintained and supported by Kitware (kitware.com/cmake).
```
