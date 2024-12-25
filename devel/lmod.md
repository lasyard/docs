# Lmod

<https://github.com/TACC/Lmod>

## Install

### By package manager

::::{plat} centos
:vers: CentOS 8.5

Need to install `tcl` and `lua` first:

```sh
sudo dnf install tcl lua
```

Then install `Lmod`:

```sh
sudo dnf install Lmod
```

:::{note}
The package name `Lmod` is case-sensitive.
:::

The traditional Tcl-based module system may be already installed, check the version:

```console
$ module --version
Modules Release 4.5.2 (2020-07-30)
```

Switch to new installed Lmod module system:

```sh
sudo alternatives --config modules.sh
```

This is effective in login profile. After re-login, check the version again:

:::{literalinclude} /_files/centos/console/ml/version.txt
:language: console
:::

::::

::::{plat} ubuntu
:vers: Ubuntu 22.04

```sh
sudo apt install lmod
```

If there is not file `/etc/profile.d/lmod.sh`:

```sh
sudo ln -snf /usr/share/lmod/6.6/init/bash /etc/profile.d/lmod.sh
```

This is effective in login profile. After re-login, check the version:

:::{literalinclude} /_files/ubuntu/console/ml/version.txt
:language: console
:::

::::

### Build from source

::::{plat} ubuntu
:vers: Ubuntu 22.04

Download the sources:

```sh
curl -L https://github.com/TACC/Lmod/archive/refs/tags/8.7.55.tar.gz -o Lmod-8.7.55.tar.gz
```

Preinstall these packages:

```sh
sudo apt install bc
sudo apt install lua5.3
sudo apt install lua-posix
sudo apt install liblua5.3-dev tcl-dev
```

```sh
tar -C ~/workspace/devel/ -xzf Lmod-8.7.55.tar.gz
cd ~/workspace/devel/Lmod-8.7.55
./configure --with-lua_include=/usr/include/lua5.3/
sudo make install
sudo ln -snf /usr/local/lmod/lmod/init/profile /etc/profile.d/lmod.sh
```

After re-login, check the version:

:::{literalinclude} /_files/ubuntu/console/ml/version_8.7.55.txt
:language: console
:::

::::

## Usage

List available modules:

```sh
ml avail
```

Or for a more consice list:

```sh
ml overview
```

List loaded modules:

```sh
ml list
```

Load a module:

```sh
ml lmod
```

Unload a module:

```sh
ml unload lmod
```
