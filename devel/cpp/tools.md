# Tools for Developing

::::{plat} linux
:vers: CentOS 8.5, Ubuntu 22.04

## ldd

Print shared object dependencies, for example:

:::{literalinclude} /_files/ubuntu/console/ldd/bin_ls.txt
:language: console
:::

## dmesg

Trace kernel messages:

```sh
sudo dmesg -kw
```

## strace

Trace the syscalls:

```sh
strace cat /dev/null
```

::::
