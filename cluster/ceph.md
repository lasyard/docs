# ceph

```sh
ceph version
```

{.cli-output}

```text
ceph version 17.2.7 (b12291d110049b2f35e32e0de30d70e9a4c060d2) quincy (stable)
```

## Usage

Show cluster id:

```sh
ceph fsid
```

Show status:

```sh
ceph status
```

:::{literalinclude} /_files/ubuntu/output/ceph/status.txt
:language: text
:class: cli-output
:::

```sh
ceph mon dump
```

:::{literalinclude} /_files/ubuntu/output/ceph/mon_dump.txt
:language: text
:class: cli-output
:::

### Volume

List volumes:

```sh
ceph fs volume ls
```

Show info of a volume:

```sh
ceph fs volume info xxxx-volume
```

List subvolume group of a volume:

```sh
ceph fs subvolumegroup ls xxxx-volume
```
