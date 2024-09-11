# Install Python Development Environment

:::{plat} ubuntu
:vers: Ubuntu 22.04

Install python:

```sh
sudo apt install python3 python3-pip
```

:::

:::{plat} msys2

```sh
pacman -S ${MINGW_PACKAGE_PREFIX}-python
pacman -S ${MINGW_PACKAGE_PREFIX}-python-pip
```

:::
