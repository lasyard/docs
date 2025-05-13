# Install Slurm Packages

## By Package Manager

:::::{tabs}
::::{group-tab} CentOS 8.5
Enable repo "PowerTools":

```console
$ sudo dnf config-manager --set-enabled powertools
```

For controller nodes:

```console
$ sudo dnf install slurm-slurmctld
```

For worker nodes:

```console
$ sudo dnf install slurm-slurmd
```

:::{tip}
Install `slurmctld` or `slurmd` will install `slurm` as dependencies.
:::

For client:

```console
$ sudo dnf install slurm
```

For accounting:

```console
$ sudo dnf install slurm-slurmdbd
```

For REST API:

```console
$ sudo dnf install slurm-slurmrestd
```

For SPANK developing:

```console
$ sudo dnf install slurm-devel
```

::::
::::{group-tab} Ubuntu 22.04
Package of slurm client is standalone on Ubuntu, install it with:

```console
$ sudo apt satisfy slurm-client
```

::::
:::::

The packages delivered are quite old.

## Build from sources

Download sources:

```console
$ curl -LO https://download.schedmd.com/slurm/slurm-24.11.5.tar.bz2
$ curl -LO https://download.schedmd.com/slurm/slurm-24.11.0.tar.bz2
```

:::::{tabs}
::::{group-tab} CentOS 8.5
:::{include} /_files/frags/toolchain/centos_gcc_11.txt
:::

See "<project:/devel/cpp/install.md>" for how to install build tools on CentOS.

Install building dependencies:

```console
$ sudo dnf install python3 hwloc-devel mariadb-devel pam-devel readline-devel libjwt-devel munge-devel perl-devel http-parser-devel json-c-devel
```

Build:

```console
$ rpmbuild -ta slurm-24.11.0.tar.bz2 --with slurmrestd
```

If the node is not where the source was building (i.e. the devel packages were installed), install these runtime packages first:

```console
$ sudo dnf install hwloc-devel libjwt mariadb-connector-c
```

Install the rpm packages, for example:

```console
$ cd ~/rpmbuild/RPMS/x86_64/
$ sudo rpm -iv slurm-24.11.0-1.el8.x86_64.rpm 
```

:::{tip}
Packages installed by `rpm` can be uninstalled by `dnf remove`.
:::
::::
::::{group-tab} Ubuntu 22.04
:::{include} /_files/frags/toolchain/ubuntu_gcc_11.txt
:::

See "<project:/devel/cpp/install.md>" for how to install build tools on Ubuntu/Debian.

Install building dependencies:

```console
$ sudo apt install libmunge-dev libmariadb-dev libhwloc-dev
```

Extract and build:

```console
$ tar -C ~/workspace/devel/ -xjf slurm-24.11.5.tar.bz2
$ cd ~/workspace/devel/slurm-24.11.5/
$ sudo mk-build-deps -i debian/control
$ debuild -b -us -uc
$ cd ..
$ ls
slurm-24.11.5                                             slurm-smd-sackd-dbgsym_24.11.5-1_amd64.ddeb
slurm-smd-client-dbgsym_24.11.5-1_amd64.ddeb              slurm-smd-sackd_24.11.5-1_amd64.deb
slurm-smd-client_24.11.5-1_amd64.deb                      slurm-smd-slurmctld-dbgsym_24.11.5-1_amd64.ddeb
slurm-smd-dbgsym_24.11.5-1_amd64.ddeb                     slurm-smd-slurmctld_24.11.5-1_amd64.deb
slurm-smd-dev_24.11.5-1_amd64.deb                         slurm-smd-slurmd-dbgsym_24.11.5-1_amd64.ddeb
slurm-smd-doc_24.11.5-1_all.deb                           slurm-smd-slurmd_24.11.5-1_amd64.deb
slurm-smd-libnss-slurm-dbgsym_24.11.5-1_amd64.ddeb        slurm-smd-slurmdbd-dbgsym_24.11.5-1_amd64.ddeb
slurm-smd-libnss-slurm_24.11.5-1_amd64.deb                slurm-smd-slurmdbd_24.11.5-1_amd64.deb
slurm-smd-libpam-slurm-adopt-dbgsym_24.11.5-1_amd64.ddeb  slurm-smd-slurmrestd-dbgsym_24.11.5-1_amd64.ddeb
slurm-smd-libpam-slurm-adopt_24.11.5-1_amd64.deb          slurm-smd-slurmrestd_24.11.5-1_amd64.deb
slurm-smd-libpmi0-dbgsym_24.11.5-1_amd64.ddeb             slurm-smd-sview-dbgsym_24.11.5-1_amd64.ddeb
slurm-smd-libpmi0_24.11.5-1_amd64.deb                     slurm-smd-sview_24.11.5-1_amd64.deb
slurm-smd-libpmi2-0-dbgsym_24.11.5-1_amd64.ddeb           slurm-smd-torque_24.11.5-1_all.deb
slurm-smd-libpmi2-0_24.11.5-1_amd64.deb                   slurm-smd_24.11.5-1_amd64.build
slurm-smd-libslurm-perl-dbgsym_24.11.5-1_amd64.ddeb       slurm-smd_24.11.5-1_amd64.buildinfo
slurm-smd-libslurm-perl_24.11.5-1_amd64.deb               slurm-smd_24.11.5-1_amd64.changes
slurm-smd-openlava_24.11.5-1_all.deb                      slurm-smd_24.11.5-1_amd64.deb
```

:::{note}
In order to use `nvml`, Slurm must be build with CUDA installed.
:::

Install the packages. For controller nodes:

```console
$ sudo dpkg -i slurm-smd_24.11.5-1_amd64.deb slurm-smd-slurmctld_24.11.5-1_amd64.deb
```

For worker nodes:

```console
$ sudo dpkg -i slurm-smd_24.11.5-1_amd64.deb slurm-smd-slurmd_24.11.5-1_amd64.deb slurm-smd-client_24.11.5-1_amd64.deb
```

:::{important}
Slurm client is required on computing nodes for it is common to using `srun` in slurm batch scripts.
:::

:::{note}
If the installation failed due to missing dependencies, fix them by:

```console
$ sudo apt install -f
```

then re-run the installation command.
:::
::::
:::::
