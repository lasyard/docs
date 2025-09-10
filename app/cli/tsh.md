# tsh

<https://goteleport.com/>

## Install

Download the packages:

::::{tab-set}

:::{tab-item} macOS

```console
$ curl -LO https://cdn.teleport.dev/tsh-16.1.0.pkg
```

:::
:::{tab-item} Linux

```console
$ curl -LO https://cdn.teleport.dev/teleport-v16.1.0-linux-amd64-bin.tar.gz
```

:::
::::

## Usage

Login:

```console
$ tsh login --proxy=xxxx.teleport --user=xxxx
Enter password for Teleport user xxxx:
Enter an OTP code from a device:
...
```

List hosts:

```console
$ tsh ls
Node Name         Address    Labels                              
----------------- ---------- ----------------------------------- 
...
```

SSH to a host:

```console
$ tsh ssh root@host-xxxx
```

Copy files to a host:

```console
$ tsh scp volcano-1.12.2.tgz root@host-xxxx:
volcano-1.12.2.tgz 100% |████████████████████████████████████████████████████████████████████████████████████████████| (81/81 kB, 9.5 MB/s)
```
