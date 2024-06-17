# Miscellaneous

## Check version

```sh
cat /etc/centos-release
```

{.cli-output}

```text
CentOS Linux release 8.5.2111
```

## List port listening

```sh
netstat -ltnp
lsof -i :6820
```

## Disable SELinux

See current status:

```sh
getenforce
```

Temporarily disable it:

```sh
setenforce 0
```

Permanently disable it:

```sh
vi /etc/selinux/config
```

:::{literalinclude} /_files/centos/etc/selinux/config
:diff: /_files/centos/etc/selinux/config.orig
:class: file-content
:::

## Set swap off

```sh
cat /proc/swaps
```

{.cli-output}

```text
Filename                                Type        Size    Used    Priority
/dev/dm-1                               partition   8269820 0       -2
```

Turn off swap for all devices:

```sh
swapoff -av
```

{.cli-output}

```text
swapoff /dev/dm-1
```

To permanently disable swap, edit `/etc/fstab` and comment out the line that mounts the swap partition.
