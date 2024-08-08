# apt

<https://www.debian.org/doc/manuals/debian-handbook/sect.apt-get.en.html>

## Usage

:::{tip}
Use `apt-get` instead of `apt` in scripts for it has stable interfaces.
:::

List installed packages:

```sh
sudo apt list --installed
```

Show info about a package:

```sh
sudo apt show libopenmpi-dev
```

Show installed files of a package:

```sh
dpkg-query -L libopenmpi-dev
```

## Popular packages

```sh
sudo apt install iputils-ping
sudo apt install iproute2
```
