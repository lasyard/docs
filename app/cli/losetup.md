# losetup

`losetup` is a Linux command to set up and control loop devices.

Create a big file for bingding:

```console
$ sudo mkdir -p /srv/ceph-test
$ sudo truncate -s 20G /srv/ceph-test/osd.0.img
```

`20G` is the size of the file, but is actually not occupied:

```console
$ ls -lh
total 0
-rw-r--r-- 1 root root 20G Apr 15 14:21 osd.0.img
```

Bind it to loop deivce:

```console
$ sudo losetup -f /srv/ceph-test/osd.0.img
```

`-f` to find an available loop device number.

List all loop devices:

```console
$ losetup
NAME       SIZELIMIT OFFSET AUTOCLEAR RO BACK-FILE                DIO LOG-SEC
/dev/loop0         0      0         0  0 /srv/ceph-test/osd.0.img   0     512
$ losetup -a
/dev/loop0: [64513]:6368 (/srv/ceph-test/osd.0.img)
```

Unbind the device:

```console
$ losetup -d /dev/loop0
```

Unbind all loop devices:

```console
$ losetup -D
```
