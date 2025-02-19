# Linux Kernel Developing

## Kernel message log level

```console
$ cat /proc/sys/kernel/printk
4       4       1       7
```

## dmesg

Trace kernel messages:

```sh
sudo dmesg -kw
```
