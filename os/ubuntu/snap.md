# snap

<https://snapcraft.io/>

```console
$ snap --version
snap    2.68.5
snapd   2.68.5
series  16
ubuntu  22.04
kernel  5.15.0-141-generic
```

List installed packages:

```console
$ snap list
Name    Version        Rev    Tracking       Publisher   Notes
core20  20250526       2599   latest/stable  canonical✓  base
lxd     5.0.4-497fe1e  31333  5.0/stable/…   canonical✓  -
snapd   2.68.5         24718  latest/stable  canonical✓  snapd
```

Packages are mounted to `/snap` using `squashfs`:

```console
$ df -a -t squashfs
Filesystem      Size  Used Avail Use% Mounted on
/dev/loop1       64M   64M     0 100% /snap/core20/2582
/dev/loop2       90M   90M     0 100% /snap/lxd/31333
/dev/loop4       51M   51M     0 100% /snap/snapd/24505
/dev/loop5       64M   64M     0 100% /snap/core20/2599
/dev/loop0       51M   51M     0 100% /snap/snapd/24718
```

Remove a package, for example, `etcd`:

```console
$ sudo snap remove etcd
etcd removed
```
