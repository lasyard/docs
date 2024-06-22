# MSYS2

<https://www.msys2.org/>

Software Distribution and Building Platform for Windows.

MSYS2 is a collection of tools and libraries providing you with an easy-to-use environment for building, installing and running native Windows software.

## Configure

Edit `C:\msys64\etc\nsswitch.conf` to set home directory to `%USERPROFILE%`:

:::{literalinclude} /_files/msys2/etc/nsswitch.conf
:diff: /_files/msys2/etc/nsswitch.conf.orig
:class: file-content
:::

## pacman

Search for a package:

```sh
pacman -Ss mediainfo
```

Install a package:

```sh
pacman -S git
pacman -S ${MINGW_PACKAGE_PREFIX}-mediainfo
pacman -S ${MINGW_PACKAGE_PREFIX}-jq
```

Update all packages:

```sh
pacman -Syu
```

## Install development tools

```sh
pacman -S make
```

### python

```sh
pacman -S ${MINGW_PACKAGE_PREFIX}-python
pacman -S ${MINGW_PACKAGE_PREFIX}-python-pip
```
