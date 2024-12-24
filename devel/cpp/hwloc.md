# hwloc

<https://www.open-mpi.org/projects/hwloc/>

## Install

### By package manager

::::{plat} centos
:vers: CentOS 8.5

```sh
sudo dnf install hwloc
sudo dnf install hwloc-devel
```

Check the version:

```console
$ lstopo --version
lstopo 2.7.1
```

:::{note}
This version is too old to support slurm 24.11.0.
:::

::::

### Build from sources

::::{plat} centos
:vers: CentOS 8.5

:::{include} /_files/frags/toolchain/centos_gcc_11.txt
:::

Download the sources:

```sh
wget https://download.open-mpi.org/release/hwloc/v2.11/hwloc-2.11.2.tar.bz2
```

```sh
tar -C ~/workspace/devel -xjf hwloc-2.11.2.tar.bz2
cd ~/workspace/devel/hwloc-2.11.2/
./configure --prefix=/usr
make -j
sudo make install
```

:::{tip}
Set prefix to `/usr` to override the rpm installed packages. Do not remove the rpm package to keep the meta-data for dependency check when installing other rpm packages.
:::

Check the version:

```console
$ lstopo --version
lstopo 2.11.2
```

::::
