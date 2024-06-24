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

## ulimit

Provides control over the resources available to the shell and to processes started by it, on systems that allow such control.

Show current limits:

```sh
ulimit -a
```

:::{literalinclude} /_files/centos/output/ulimit/a.txt
:language: text
:class: cli-output
:::

Set the maximum number of open files:

```sh
ulimit -n 1048576
```

This is effective only in current shell and any child processes. To make it permanent:

```sh
vi /etc/security/limits.conf
```

:::{literalinclude} /_files/centos/etc/security/limits.conf.orig
:language: text
:class: file-content
:::

The modification will take effect after a re-login.

:::{note}
If there are file in `/etc/security/limits.d`, the values may be overridden by those files.
:::

The limits are applied by a per-process manner. You can check the limits for process 1 (i.e. the init process):

```sh
cat /proc/1/limits
```

:::{literalinclude} /_files/centos/output/cat/proc_1_limits.txt
:language: text
:class: cli-output
:::
