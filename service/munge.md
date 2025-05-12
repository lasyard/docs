# munge

<https://dun.github.io/munge/>

## Install

::::{tabs}
:::{group-tab} CentOS 8.5

```console
$ sudo dnf install munge
```

Check the version:

```console
$ munge --version
munge-0.5.13 (2017-09-26)
```

:::
:::{group-tab} Ubuntu 22.04

```console
$ sudo apt install munge
```

Check the version:

```console
$ munge --version
munge-0.5.14 (2020-01-14)
```

:::
::::

## Configure

On one node:

::::{tabs}
:::{group-tab} CentOS 8.5

```console
$ sudo create-munge-key
```

:::
:::{group-tab} Ubuntu 22.04

```console
$ sudo -u munge -g munge mungekey -cf
```

:::
::::

The generated key file is `/etc/munge/munge.key` by default. Copy it to all nodes. Be careful with the file owner, group and modes.

## Run

::::{tabs}
:::{group-tab} CentOS 8.5

```console
$ sudo systemctl enable munge --now
```

:::
:::{group-tab} Ubuntu 22.04

Restart the service after the key is re-generated:

```console
$ sudo systemctl restart munge
```

:::
::::

## Usage

Test it:

```console
$ munge -n
MUNGE:AwQFAAAxoR8LtzIKZyzZrqT79ukWuP+aoUOE5FglyC6+JEOGfBRdHM9TGKJvcTIqVOvUdCnPhq/qthbgO+kCuxYktZYbBFxUlwICISq36r5DvXL1KF3NXx5t5EyK4e0Y/PQmYrU=:
```

List the compression type supported:

```console
$ munge -Z
Compression types:

  none (0)
  default (1)
  bzlib (2)
  zlib (3)
```

Remote authentication (with file payload):

```console
$ munge -i /etc/hostname | ssh las1 unmunge
STATUS:          Success (0)
ENCODE_HOST:     las0 (10.225.4.51)
ENCODE_TIME:     2025-05-09 16:45:09 +0800 (1746780309)
DECODE_TIME:     2025-05-09 16:45:07 +0800 (1746780307)
TTL:             300
CIPHER:          aes128 (4)
MAC:             sha256 (5)
ZIP:             none (0)
UID:             ubuntu (1000)
GID:             ubuntu (1000)
LENGTH:          6

las0
```
