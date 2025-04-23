# MSYS2

<https://www.msys2.org/>

## Configure

Edit `C:\msys64\etc\nsswitch.conf` to set home directory to `%USERPROFILE%`:

:::{literalinclude} /_files/windows/msys2/etc/nsswitch.conf
:diff: /_files/windows/msys2/etc/nsswitch.conf.orig
:::

## pacman

Search for a package:

```sh
pacman -Ss mediainfo
```

Install a package:

```sh
pacman -S git
pacman -S ${MINGW_PACKAGE_PREFIX}-ffmpeg
pacman -S ${MINGW_PACKAGE_PREFIX}-mediainfo
pacman -S ${MINGW_PACKAGE_PREFIX}-jq
```

Update all packages:

```sh
pacman -Syu
```
