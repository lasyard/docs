# Tools for Developing

::::{plat} linux
:vers: CentOS 8.5, Ubuntu 22.04

## ldd

Print shared object dependencies, for example:

:::{literalinclude} /_files/ubuntu/console/ldd/bin_ls.txt
:language: console
:::

## strace

Trace the syscalls:

```sh
strace cat /dev/null
```

## journalctl

See messages:

```sh
journalctl -f
```

If you have admin previlege, you can see the kernel messages.

See only kernel messages:

```sh
sudo journalctl -k -f
```

::::
