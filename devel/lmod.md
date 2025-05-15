# Lmod

<https://github.com/TACC/Lmod>

## Install

### By package manager

:::::{tabs}
::::{group-tab} CentOS 8.5
Install `tcl` and `lua` first:

```console
$ sudo dnf install tcl lua
```

Then install `Lmod`:

```console
$ sudo dnf install Lmod
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

```console
$ sudo alternatives --config modules.sh
```

This is effective in login profile. After re-login, check the version again:

```console
$ module --version

Modules based on Lua: Version 8.7.53 2024-10-12 19:57 -05:00
    by Robert McLay mclay@tacc.utexas.edu
```

::::
::::{group-tab} Ubuntu 22.04

```console
$ sudo apt install lmod
```

The installation will create login script file `/etc/profile.d/lmod.sh`. After re-login, check the version:

```console
$ ml --version

Modules based on Lua: Version 6.6  2016-10-13 13:28 -05:00
    by Robert McLay mclay@tacc.utexas.edu
```

::::
:::::

### Build from source

Download the sources:

```console
$ curl -L https://github.com/TACC/Lmod/archive/refs/tags/8.7.60.tar.gz -o Lmod-8.7.60.tar.gz
```

::::{tabs}
:::{group-tab} Ubuntu 22.04
:::{include} /_files/frags/toolchain/ubuntu_gcc_11.txt
:::
Preinstall these packages:

```console
$ sudo apt install bc lua5.3 lua-posix liblua5.3-dev tcl-dev
```

Extract the sources and build:

```console
$ tar -C ~/workspace/devel/ -xzf Lmod-8.7.60.tar.gz
$ cd ~/workspace/devel/Lmod-8.7.60
$ ./configure --with-lua_include=/usr/include/lua5.3/
$ sudo make install
```

Create/replace the profile script:

```console
$ sudo ln -snf /usr/local/lmod/lmod/init/profile /etc/profile.d/lmod.sh
```

After re-login, check the version:

```console
$ ml --version

Modules based on Lua: Version 8.7.60 2025-04-30 12:50 -05:00
    by Robert McLay mclay@tacc.utexas.edu
```

:::
::::

## Usage

List available modules:

```console
$ ml avail

------------------------------------------------------ /usr/local/lmod/lmod/modulefiles/Core -------------------------------------------------------
   lmod    settarg

If the avail list is too long consider trying:

"module --default avail" or "ml -d av" to just list the default modules.
"module overview" or "ml ov" to display the number of modules for each name.

Use "module spider" to find all possible modules and extensions.
Use "module keyword key1 key2 ..." to search for all possible modules matching any of the "keys".
```

Or for a more consice list:

```console
$ ml ov

------------------------------------------------------ /usr/local/lmod/lmod/modulefiles/Core -------------------------------------------------------
lmod (1)   settarg (1)
```

List loaded modules:

```console
$ ml list
No modules loaded
```

Load a module:

```console
$ ml lmod
$ ml list

Currently Loaded Modules:
  1) lmod
```

Unload a module:

```console
$ ml unload lmod
$ ml list
No modules loaded
```
