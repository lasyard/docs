# Install Slurm Packages

## By Package Manager

::::{plat} centos
:vers: CentOS 8.5

```sh
sudo dnf config-manager --set-enabled powertools
dnf repolist powertools
```

:::{literalinclude} /_files/centos/output/dnf/repolist_powertools.txt
:language: text
:class: cli-output
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
sudo apt update
sudo apt satisfy slurm-client
```

::::

## Build from sources

Download sources:

```sh
wget https://download.schedmd.com/slurm/slurm-24.05.1.tar.bz2
```

::::{plat} centos
:vers: CentOS 8.5
The toolchain used:

- gcc 11.2.1
- GNU Make 4.3
- rpmbuild 4.14.3

See "<project:/devel/cpp/install.md>" for how to install build tools on CentOS.

Install building dependencies:

```sh
sudo dnf install mariadb-devel pam-devel readline-devel libjwt-devel
```

Build:

```sh
rpmbuild -ta slurm-24.05.1.tar.bz2
```

If the node is not where the source was building (i.e. the devel packages were installed), install these runtime packages first:

```sh
sudo dnf install libjwt mariadb-connector-c
```

Install the rpm packages, for instance:

```sh
cd ~/rpmbuild/RPMS/x86_64/
sudo rpm -iv slurm-24.05.1-1.el8.x86_64.rpm 
```

:::{tip}
Packages installed by `rpm` can be uninstalled by `dnf remove`.
:::

::::

::::{plat} ubuntu
:vers: Ubuntu 22.04

The toolchain used:

- gcc 11.4.0
- GNU Make 4.3
- debuild 2.22.1ubuntu1

See "<project:/devel/cpp/install.md>" for how to install build tools on Ubuntu/Debian.

```sh
tar -xjf slurm-24.05.1.tar.bz2
cd slurm-24.05.1/
sudo mk-build-deps -i debian/control
debuild -b -us -uc
cd ..
```

Install the packages, for instance:

```sh
sudo dpkg -i slurm-smd_24.05.1-1_amd64.deb
```

:::{note}
If the installation failed due to missing dependencies, fix them by

```sh
sudo apt install -f
```

then re-run the installation command.
:::

::::
