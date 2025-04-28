# Tools for Developing

These tools are mostly used on Linux, for example, CentOS 8.5 and Ubuntu 22.04.

## ldd

Print shared object dependencies, for example:

```console
$ ldd /bin/ls
    linux-vdso.so.1 (0x00007ffe33b7d000)
    libselinux.so.1 => /lib/x86_64-linux-gnu/libselinux.so.1 (0x00007f4fe44dd000)
    libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f4fe42b4000)
    libpcre2-8.so.0 => /lib/x86_64-linux-gnu/libpcre2-8.so.0 (0x00007f4fe421d000)
    /lib64/ld-linux-x86-64.so.2 (0x00007f4fe4534000)
```

## strace

Trace the syscalls, for example:

```console
$ strace -e openat cat /dev/null
openat(AT_FDCWD, "/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libc.so.6", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "/usr/lib/locale/locale-archive", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "/usr/share/locale/locale.alias", O_RDONLY|O_CLOEXEC) = 3
...
```

In which the `-e openat` filter in only `openat` syscall.

## journalctl

See system logs:

```console
$ journalctl -f
```

If you have admin previlege, you can see the kernel messages.

See only kernel messages:

```console
$ sudo journalctl -k -f
```

## dmesg

Show kernel logs:

```console
$ sudo dmesg -w
```

See the log levels:

```console
$ cat /proc/sys/kernel/printk
4       4       1       7
```

The result shows the current, default, minimum and boot-time-default log levels.

Modify the current log level:

```console
$ echo 8 | sudo tee /proc/sys/kernel/printk
```

This command turns on all messages.

See <https://www.kernel.org/doc/html/latest/core-api/printk-basics.html> for details.
