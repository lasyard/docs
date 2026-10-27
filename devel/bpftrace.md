# bpftrace

<https://ebpf.io/>

## Install

:::::{tab-set}
::::{tab-item} Ubuntu
:sync: ubuntu

```console
$ sudo apt install bpftrace
```

```console
$ bpftrace --version
bpftrace v0.14.0
```

::::
:::::

## Usage

```sh
sudo bpftrace -e 'tracepoint:syscalls:sys_enter_openat {
  printf("%s opened %s\n", comm, str(args->filename));
}'
```
