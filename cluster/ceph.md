# ceph

## Install

### cephadm

::::{tab-set}
:::{tab-item} Ubuntu 22.04

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
cephadm version 19.2.2 (0eceb0defba60152a8182f7bd87d164b639885b8) squid (stable)
```

### Client

```console
$ sudo cephadm install ceph-common
Installing packages ['ceph-common']...
```

You can also use the package manager to install it from the repository for your platform.

## Deploy

Bootstrap a cluster using `cephadm`:

```console
$ sudo cephadm bootstrap --mon-ip 10.225.4.54 --cluster-network 10.225.4.0/24
Verifying podman|docker is present...
Verifying lvm2 is present...
Verifying time synchronization is in place...
Unit systemd-timesyncd.service is enabled and running
Repeating the final host check...
docker (/usr/bin/docker) is present
systemctl is present
lvcreate is present
Unit systemd-timesyncd.service is enabled and running
Host looks OK
Cluster fsid: c0accb9e-37c2-11f0-af12-3738f6ab3838
...
Pulling container image quay.io/ceph/ceph:v19...
Ceph version: ceph version 19.2.2 (0eceb0defba60152a8182f7bd87d164b639885b8) squid (stable)
...
Ceph Dashboard is now available at:

         URL: https://las3:8443/
        User: admin
    Password: xxxxxxxxxx

Enabling client.admin keyring and conf on hosts with "admin" label
Saving cluster configuration to /var/lib/ceph/c0accb9e-37c2-11f0-af12-3738f6ab3838/config directory
You can access the Ceph CLI as following in case of multi-cluster or non-default config:

    sudo /usr/sbin/cephadm shell --fsid c0accb9e-37c2-11f0-af12-3738f6ab3838 -c /etc/ceph/ceph.conf -k /etc/ceph/ceph.client.admin.keyring

Or, if you are only running a single cluster on this host:

    sudo /usr/sbin/cephadm shell 

Please consider enabling telemetry to help improve Ceph:

    ceph telemetry on

For more information see:

    https://docs.ceph.com/en/latest/mgr/telemetry/

Bootstrap complete.
```

The files created in directory `/etc/ceph` is not used by the ceph cluster deployed above, for they are running in containers, but for the `ceph` command on the host. Change the owner and permissions to make it available for the current user `ubuntu`:

```console
$ sudo chown ceph:ceph /etc/ceph/ceph.client.admin.keyring
$ sudo chmod g+r /etc/ceph/ceph.client.admin.keyring
$ sudo usermod -aG ceph ubuntu
$ cat /etc/ceph/ceph.client.admin.keyring
```

Show the version using `ceph`:

```console
$ ceph version
ceph version 19.2.2 (0eceb0defba60152a8182f7bd87d164b639885b8) squid (stable)
```

:::{tip}
The following command can destroy the `ceph` things installed by `cephadm` on a node:

```console
$ sudo cephadm rm-cluster --force --zap-osds --fsid $(ceph fsid)
Deleting cluster with fsid: c0accb9e-37c2-11f0-af12-3738f6ab3838
...
```

:::

:::{admonition} TODO
`ceph status` is not healthy.
:::

## Usage

Use cephadm shell:

```console
$ sudo cephadm shell
Inferring fsid 8e6bf37e-37ba-11f0-af12-3738f6ab3838
Inferring config /var/lib/ceph/8e6bf37e-37ba-11f0-af12-3738f6ab3838/mon.las3/config
Using ceph image with id '259b35566514' and tag 'v17' created on 2024-11-26 08:45:38 +0800 CST
quay.io/ceph/ceph@sha256:a0f373aaaf5a5ca5c4379c09da24c771b8266a09dc9e2181f90eacf423d7326f
...
```

The `cephadm shell` commnad run a container with `ceph` client installed and mount the required files in `/etc/ceph` in, so `ceph` command is available in it.

### Show info

```sh
ceph fsid
```

```sh
ceph status
```

```sh
ceph mon dump
```

### Volume

List volumes:

```sh
ceph fs volume ls
```

Show info of a volume:

```sh
ceph fs volume info xxxx-volume
```

List subvolume group of a volume:

```sh
ceph fs subvolumegroup ls xxxx-volume
```
