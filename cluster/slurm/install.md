# Install Slurm Packages

## Using dnf on CentOS

```sh
dnf config-manager --set-enabled powertools
dnf repolist powertools
```

:::{literalinclude} /_files/centos/output/dnf/repolist_powertools.txt
:language: text
:class: cli-output
:::

For controller node:

```sh
dnf install slurm-slurmctld
```

For compute nodes:

```sh
dnf install slurm-slurmd
```

:::{tip}
Install `slurmctld` or `slurmd` will install `slurm` as dependencies.
:::

For client:

```sh
dnf install slurm
```

For SPANK developing:

```sh
dnf install slurm-devel
```

For accounting and REST API:

```sh
dnf install slurm-slurmdbd
dnf install slurm-slurmrestd
```

## Using apt on Ubuntu/Debian

Package of slurm client is standalone on Debian/Ubuntu, install it with:

```sh
sudo apt update
sudo apt satisfy slurm-client
```

## Build from sources

Download sources:

```sh
wget https://download.schedmd.com/slurm/slurm-23.11.7.tar.bz2
```

{{ for_centos }}

{{ centos_build }}

See "<project:/os/CentOS/devel.md>" for how to install build tools on CentOS.

Install building dependencies:

```sh
dnf install mariadb-devel pam-devel readline-devel libjwt-devel
```

Build:

```sh
rpmbuild -ta slurm-23.11.7.tar.bz2
```

If the node is not where the source was building (i.e. the devel packages were installed), install these runtime packages first:

```sh
dnf install libjwt mariadb-connector-c
```

Install the rpm packages:

```sh
cd ~/rpmbuild/RPMS/x86_64/
rpm -iv slurm-23.11.7-1.el8.x86_64.rpm 
rpm -iv slurm-slurmctld-23.11.7-1.el8.x86_64.rpm 
rpm -iv slurm-slurmdbd-23.11.7-1.el8.x86_64.rpm
rpm -iv slurm-slurmd-23.11.7-1.el8.x86_64.rpm
```

:::{tip}
Packages installed by `rpm` can be uninstalled by `dnf remove`.
:::

{{ for_ubuntu }}

{{ ubuntu_build }}

See "<project:/os/Ubuntu/devel.md>" for how to install build tools on Ubuntu/Debian.

```sh
tar -xjf slurm-23.11.7.tar.bz2
cd slurm-23.11.7/
sudo mk-build-deps -i debian/control
debuild -b -us -uc
cd ..
```

Install the packages:

```sh
sudo dpkg -i slurm-smd_23.11.7-1_amd64.deb
sudo dpkg -i slurm-smd-client_23.11.7-1_amd64.deb
```

:::{note}
If the installation failed due to missing dependencies, fix them by

```sh
sudo apt install -f
```

then re-run the installation command.
:::
