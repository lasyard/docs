# Install Python Development Environment

## By package manager

::::{plat} ubuntu
:vers: Ubuntu 22.04

Install python:

```sh
sudo apt install python3 python3-pip
```

::::

::::{plat} msys2

```sh
pacman -S ${MINGW_PACKAGE_PREFIX}-python
pacman -S ${MINGW_PACKAGE_PREFIX}-python-pip
```

::::

## Build from sources

::::{plat} centos
:vers: CentOS 8.5

Download sources:

```sh
wget https://www.python.org/ftp/python/3.10.14/Python-3.10.14.tgz
```

```sh
tar -C ~/workspace/devel/ -xzf Python-3.10.14.tgz
cd ~/workspace/devel/Python-3.10.14/
```

Install some packages before building:

```sh
sudo dnf install -y libffi-devel zlib-devel bzip2-devel xz-devel openssl-devel uuid-devel sqlite-devel libnsl2-devel
```

Configure and build:

```sh
./configure --enable-optimizations
make -j
sudo make install
```

```sh
sudo ln -snf pip3.10 /usr/local/bin/pip3
sudo ln -snf pip3.10 /usr/local/bin/pip
```

::::
