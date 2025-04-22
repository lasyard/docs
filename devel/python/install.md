# Install Python Development Environment

## By package manager

::::{tabs}
:::{tab} Ubuntu 22.04

```console
$ sudo apt install python3 python3-pip
```

:::
:::{tab} MSYS2

```console
$ pacman -S ${MINGW_PACKAGE_PREFIX}-python
$ pacman -S ${MINGW_PACKAGE_PREFIX}-python-pip
```

:::
::::

## Build from sources

Download sources:

```console
$ curl -LO https://www.python.org/ftp/python/3.10.14/Python-3.10.14.tgz
```

::::{tabs}
:::{tab} CentOS 8.5

Extract files:

```console
$ tar -C ~/workspace/devel/ -xzf Python-3.10.14.tgz
$ cd ~/workspace/devel/Python-3.10.14/
```

Install dependent packages before building:

```console
$ sudo dnf install -y libffi-devel zlib-devel bzip2-devel xz-devel openssl-devel uuid-devel sqlite-devel libnsl2-devel
```

Configure, build and install:

```console
$ ./configure --enable-optimizations
$ make -j
$ sudo make install
```

Create symbolic links:

```console
$ sudo ln -snf pip3.10 /usr/local/bin/pip3
$ sudo ln -snf pip3.10 /usr/local/bin/pip
```

:::
::::
