# Miscellaneous

## Check version

```console
$ cat /etc/centos-release
CentOS Linux release 8.5.2111
```

## Disable SELinux

See current status:

```console
$ getenforce
```

Temporarily disable it:

```console
$ sudo setenforce 0
```

To permanently disable it, you can edit file `/etc/selinux/config`:

:::{literalinclude} /_files/centos/etc/selinux/config
:diff: /_files/centos/etc/selinux/config.orig
:::

## Set swap off

Show devices with swap enabled:

```console
$ cat /proc/swaps
Filename                                Type        Size    Used    Priority
/dev/dm-1                               partition   8269820 0       -2
```

Turn off swap for all devices:

```console
$ sudo swapoff -av
swapoff /dev/dm-1
```

To permanently disable swap, edit `/etc/fstab` and comment out the line that mounts the swap partition.

## ulimit

Show current limits:

```console
$ ulimit -a
core file size          (blocks, -c) 0
data seg size           (kbytes, -d) unlimited
scheduling priority             (-e) 0
file size               (blocks, -f) unlimited
pending signals                 (-i) 63176
max locked memory       (kbytes, -l) 64
max memory size         (kbytes, -m) unlimited
open files                      (-n) 1024
pipe size            (512 bytes, -p) 8
POSIX message queues     (bytes, -q) 819200
real-time priority              (-r) 0
stack size              (kbytes, -s) 8192
cpu time               (seconds, -t) unlimited
max user processes              (-u) 63176
virtual memory          (kbytes, -v) unlimited
file locks                      (-x) unlimited
```

Set the maximum number of open files:

```console
$ ulimit -n 1048576
```

This is effective only in current shell and any child processes. To make it permanent, you need to edit file `/etc/security/limits`:

:::{literalinclude} /_files/centos/etc/security/limits.conf
:language: text
:::

The modification will take effect after a re-login.

:::{note}
If there are files in `/etc/security/limits.d`, the values may be overridden by those files.
:::

The limits are applied by a per-process manner. You can check the limits for process 1 (i.e. the init process):

```console
$ cat /proc/1/limits
Limit                     Soft Limit           Hard Limit           Units
Max cpu time              unlimited            unlimited            seconds
Max file size             unlimited            unlimited            bytes
Max data size             unlimited            unlimited            bytes
Max stack size            8388608              unlimited            bytes
Max core file size        unlimited            unlimited            bytes
Max resident set          unlimited            unlimited            bytes
Max processes             63176                63176                processes
Max open files            1048576              1048576              files
Max locked memory         67108864             67108864             bytes
Max address space         unlimited            unlimited            bytes
Max file locks            unlimited            unlimited            locks
Max pending signals       63176                63176                signals
Max msgqueue size         819200               819200               bytes
Max nice priority         0                    0
Max realtime priority     0                    0
Max realtime timeout      unlimited            unlimited            us
```

## alternatives

```console
$ alternatives --version
alternatives（备用）版本 1.19.1
```

List all software managed by alternatives:

```console
$ alternatives --list
```

Config a software:

```console
$ sudo alternatives --config modules.sh
```
