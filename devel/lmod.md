# Lmod

<https://sourceforge.net/projects/lmod/>

Lmod is a Lua based module system. Modules allow for dynamic modification of a user's environment under Unix systems.

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

After installation, switch `module` command to use Lmod's:

```sh
sudo alternatives --config modules.sh
```

Check the version:

```sh
ml --version
```

:::{literalinclude} /_files/centos/output/ml/version.txt
:language: text
:class: cli-output
:::

::::

::::{plat} ubuntu
:vers: Ubuntu 22.04

```sh
sudo apt install lmod
```

Check the version:

```sh
ml --version
```

:::{literalinclude} /_files/ubuntu/output/ml/version.txt
:language: text
:class: cli-output
:::

::::

### Build from source

::::{plat} ubuntu
:vers: Ubuntu 22.04

Preinstall these packages:

```sh
sudo apt install lua5.3 tcl-dev liblua5.3-dev
sudo apt install lua-posix
```

```sh
tar -C ~/workspace/devel/ -xjvf Lmod-8.7.tar.bz2
cd ~/workspace/devel/Lmod-8.7
./configure --with-lua_include=/usr/include/lua5.3/
sudo make install
sudo ln -snf /usr/local/lmod/lmod/init/profile /etc/profile.d/lmod.sh
```

Show the new installed version:

```sh
ml --version
```

:::{literalinclude} /_files/ubuntu/output/ml/version_8.7.txt
:language: text
:class: cli-output
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
