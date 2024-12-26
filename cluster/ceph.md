# ceph

## Usage

### Show version

```console
$ ceph version
ceph version 19.2.0 (16063ff2022298c9300e49a547a16ffda59baf13) squid (stable)
```

### Show info

```sh
ceph fsid
```

```sh
ceph status
```

```sh
ceph mon dump
```

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
