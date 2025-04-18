# apt

<https://www.debian.org/doc/manuals/debian-handbook/sect.apt-get.en.html>

## Usage

:::{tip}
Use `apt-get` instead of `apt` in scripts for it has stable interfaces.
:::

List installed packages:

```console
$ sudo apt list --installed
```

Show info about a package:

```console
$ sudo apt show libopenmpi-dev
```

Show installed files of a package:

```console
$ dpkg-query -L libopenmpi-dev
```

List files in a deb package:

```console
$ dpkg-deb -c slurm-smd_24.05.4-1_amd64.deb
```

Show info of a deb package:

```console
$ dpkg-deb -f slurm-smd-client_24.05.4-1_amd64.deb
```

Find the package which contains a file:

```console
$ dpkg -S $(which file)
```

## Popular packages

### Networking

```console
$ sudo apt install iputils-ping iproute2
```

### File

```console
$ sudo apt install attr
```

### CUDA

```console
$ sudo apt install nvidia-cuda-toolkit
```
