# Install Ceph Packages

## Install cephadm

::::{tab-set}
:::{tab-item} Ubuntu 22.04
:sync: ubuntu

```console
$ sudo apt install cephadm
```

This one is too old to have a working `version` command. Use a new one in `ceph`'s own repository.
:::
::::

Add ceph repository:

```console
$ sudo cephadm add-repo --release squid
Installing repo GPG key from https://download.ceph.com/keys/release.gpg...
Installing repo file at /etc/apt/sources.list.d/ceph.list...
Updating package list...
Completed adding repo.
```

:::{tip}
The repo can be removed by:

```console
$ sudo cephadm rm-repo
Removing repo GPG key /etc/apt/trusted.gpg.d/ceph.release.gpg...
Removing repo at /etc/apt/sources.list.d/ceph.list...
```

:::

Then update `cephadm` itself:

```console
$ sudo cephadm install
Installing packages ['cephadm']...
```

Now show the version:

```console
$ cephadm version
cephadm version 19.2.3 (c92aebb279828e9c3c1f5d24613efca272649e62) squid (stable)
```

## Install ceph client

```console
$ sudo cephadm install ceph-common
Installing packages ['ceph-common']...
```

Show ceph client version:

```console
$ ceph --version
ceph version 19.2.3 (c92aebb279828e9c3c1f5d24613efca272649e62) squid (stable)
```

You can also use the package manager to install it from the repository for your platform:

::::{tab-set}
:::{tab-item} Ubuntu 22.04
:sync: ubuntu

```console
$ sudo apt install ceph-common
```

Show ceph client version:

```console
$ ceph --version
ceph version 17.2.9 (69bf48f20731a4b0d742613f6c6335ccb54dd217) quincy (stable)
```

:::
::::
