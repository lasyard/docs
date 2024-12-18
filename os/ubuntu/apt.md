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

List files in a deb package:

```sh
dpkg-deb -c slurm-smd_24.05.4-1_amd64.deb
```

Show info of a deb package:

```sh
dpkg-deb -f slurm-smd-client_24.05.4-1_amd64.deb
```

Find the package which contains a file:

```sh
dpkg -S $(which file)
```

## Popular packages

### Networking

```sh
sudo apt install iputils-ping
sudo apt install iproute2
```

### File

```sh
sudo apt install attr
```

### CUDA

```sh
sudo apt install nvidia-cuda-toolkit
```
