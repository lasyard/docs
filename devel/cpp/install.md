# Install C/C++ Development Environment

::::{tabs}
:::{tab} CentOS 8.5
Install the package group:

```console
$ sudo dnf group install "Development Tools"
```

The installed `gcc` compiler is quite old. You may need to install a new build tool set:

```console
$ sudo dnf install gcc-toolset-11-toolchain
```

[`scl-utils`](https://github.com/sclorg/scl-utils) is used to manage this software, try:

```console
$ scl list-collections
gcc-toolset-11
```

To use the toolset in a new shell session, run:

```console
$ scl enable gcc-toolset-11 bash
```

This command will open a new shell. You can just do the following in the current shell:

```console
$ . scl_source enable gcc-toolset-11
```

You can put the above command in your login scripts.

For `rpmbuild`, the tool itself and a gcc toolset plugin is needed:

```console
$ sudo dnf install rpm-build
$ sudo dnf install gcc-toolset-11-annobin-plugin-gcc
```

Install other tools:

```console
$ sudo dnf install autoconf automake libtool
```

Install clang tools (clang-format, clang-tidy, etc.):

```console
$ sudo dnf install clang-tools-extra
```

:::
:::{tab} Ubuntu 22.04
Install build essenstial:

```console
$ sudo apt satisfy build-essential
```

Install kernel headers if you need to compile kernel modules:

```console
$ sudo apt satisfy linux-headers-$(uname -r)
```

Install other tools:

```console
$ sudo apt install automake
$ sudo apt satisfy fakeroot devscripts
```

If you want to build deb packages, you need to install `equivs`:

```console
$ sudo apt satisfy equivs
```

:::
:::{tab} macOS Monterey
macOS has `clang` installed, but you can install a new version by:

```console
$ brew install llvm
```

If `gcc` is required:

```console
$ brew install gcc
```

You need to create symbol links manually:

```console
$ ln -snf gcc-14 /usr/local/bin/gcc
$ ln -snf g++-14 /usr/local/bin/g++
```

:::
:::{tab} MSYS2

```console
$ pacman -S make
```

:::
::::
