# Install C/C++ Development Environment

::::{plat} centos
:vers: CentOS 8.5

Install the package group:

```sh
sudo dnf group install "Development Tools"
```

The installed `gcc` compiler is quite old. You may need to install a new build tool set:

```sh
sudo dnf install gcc-toolset-11-toolchain
```

[`scl-utils`](https://github.com/sclorg/scl-utils) is used to manage this software, try:

```console
$ scl list-collections
gcc-toolset-11
```

To use the toolset in a new shell session, run:

```sh
scl enable gcc-toolset-11 bash
```

This command will open a new shell. You can just do the following in the current shell:

```sh
. scl_source enable gcc-toolset-11
```

You can put the above command in your login scripts.

For `rpmbuild`, the tool itself and a gcc toolset plugin is needed:

```sh
sudo dnf install rpm-build
sudo dnf install gcc-toolset-11-annobin-plugin-gcc
```

Install other tools:

```sh
sudo dnf install autoconf automake libtool
```

Install clang tools (clang-format, clang-tidy, etc.):

```sh
sudo dnf install clang-tools-extra
```

::::

::::{plat} ubuntu
:vers: Ubuntu 22.04

Install build essenstial:

```sh
sudo apt satisfy build-essential
```

Install kernel headers if you need to compile kernel modules:

```sh
sudo apt satisfy linux-headers-$(uname -r)
```

Install other tools:

```sh
sudo apt satisfy fakeroot devscripts
```

If you want to build deb packages, you need to install `equivs`:

```sh
sudo apt satisfy equivs
```

::::

::::{plat} msys2

```sh
pacman -S make
```

::::
