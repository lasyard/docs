# Install Slurm Packages

## By Package Manager

::::{plat} centos
:vers: CentOS 8.5

Enable repo "PowerTools":

:::{literalinclude} /_files/centos/console/dnf/repolist_powertools.txt
:language: console
:::

For controller nodes:

```sh
sudo dnf install slurm-slurmctld
```

For worker nodes:

```sh
sudo dnf install slurm-slurmd
```

:::{tip}
Install `slurmctld` or `slurmd` will install `slurm` as dependencies.
:::

For client:

```sh
sudo dnf install slurm
```

For SPANK developing:

```sh
sudo dnf install slurm-devel
```

For accounting and REST API:

```sh
sudo dnf install slurm-slurmdbd
sudo dnf install slurm-slurmrestd
```

::::

::::{plat} ubuntu
:vers: Ubuntu 22.04

Package of slurm client is standalone on Ubuntu, install it with:

```sh
sudo apt satisfy slurm-client
```

::::

## Build from sources

Download sources:

```sh
wget https://download.schedmd.com/slurm/slurm-24.11.0.tar.bz2
```

::::{plat} centos
:vers: CentOS 8.5

:::{include} /_files/frags/toolchain/centos_gcc_11.txt
:::

See "<project:/devel/cpp/install.md>" for how to install build tools on CentOS.

Install building dependencies:

```sh
sudo dnf install python3 hwloc-devel mariadb-devel pam-devel readline-devel libjwt-devel munge-devel perl-devel http-parser-devel json-c-devel
```

Build:

```sh
rpmbuild -ta slurm-24.11.0.tar.bz2 --with slurmrestd
```

If the node is not where the source was building (i.e. the devel packages were installed), install these runtime packages first:

```sh
sudo dnf install hwloc-devel libjwt mariadb-connector-c
```

Install the rpm packages, for instance:

```sh
cd ~/rpmbuild/RPMS/x86_64/
sudo rpm -iv slurm-24.11.0-1.el8.x86_64.rpm 
```

:::{tip}
Packages installed by `rpm` can be uninstalled by `dnf remove`.
:::

::::

::::{plat} ubuntu
:vers: Ubuntu 22.04

:::{include} /_files/frags/toolchain/ubuntu_gcc_11.txt
:::

See "<project:/devel/cpp/install.md>" for how to install build tools on Ubuntu/Debian.

Install building dependencies:

```sh
sudo apt install libmunge-dev libmariadb-dev libhwloc-dev
```

Extract and build:

```sh
tar -xjf slurm-24.11.0.tar.bz2
cd slurm-24.11.0/
sudo mk-build-deps -i debian/control
debuild -b -us -uc
cd ..
```

Install the packages, for instance:

```sh
sudo dpkg -i slurm-smd_24.05.1-1_amd64.deb
```

:::{note}
If the installation failed due to missing dependencies, fix them by:

```sh
sudo apt install -f
```

then re-run the installation command.
:::

::::
