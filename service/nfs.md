# NFS

## Install

::::{tabs}
:::{group-tab} Ubuntu 22.04

```console
$ sudo apt install nfs-kernel-server
```

:::
::::

## Configure

Create a directory for NFS:

```console
$ sudo mkdir /srv/nfs
```

Edit file `/etc/exports` to export the directory:

:::{literalinclude} /_files/ubuntu/etc/exports
:diff: /_files/ubuntu/etc/exports.orig
:::

Apply the new config:

```console
$ sudo exportfs -av
exporting *:/srv/nfs
```

Show the exported directories:

```console
$ sudo exportfs -v
/srv/nfs        <world>(async,wdelay,hide,no_subtree_check,sec=sys,rw,secure,no_root_squash,no_all_squash)
```

## Usage

On a client, you need to install the NFS tools:

::::{tabs}
:::{group-tab} Ubuntu 22.04

```console
$ sudo apt install nfs-common
```

:::
::::

Then do mounting:

```console
$ sudo mount las0:/srv/nfs /mnt
```
