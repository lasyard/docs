# eBPF

## Install

:::::{tab-set}
::::{tab-item} Ubuntu

For `bpftool`:

```console
$ sudo apt install linux-tools-$(uname -r)
```

```console
$ bpftool version
/usr/lib/linux-tools/5.15.0-190-generic/bpftool v5.15.209
features:
```

For C development:

```console
$ sudo apt install libbpf-dev
```

::::
:::::
