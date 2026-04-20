# Use Ceph

## Dashboard

```console
$ ceph mgr module enable dashboard
module 'dashboard' is already enabled
```

It is enabled by default, but the listening port is only bind to address of ceph internal network. To make it bind to all addresses:

```console
$ ceph config set mgr mgr/dashboard/server_addr 0.0.0.0
```

In the dashboard, you can do many things other than monitor the culster if you are `admin`.

## Show information

```console
$ ceph fsid
990b5070-3964-11f1-8888-476de7d3e05c
```

```console
$ ceph mon dump
epoch 3
fsid 990b5070-3964-11f1-8888-476de7d3e05c
last_changed 2026-04-16T10:42:57.301680+0000
created 2026-04-16T07:19:36.819230+0000
min_mon_release 19 (squid)
election_strategy: 1
0: [v2:10.225.4.54:3300/0,v1:10.225.4.54:6789/0] mon.las3
1: [v2:10.225.4.53:3300/0,v1:10.225.4.53:6789/0] mon.las2
2: [v2:10.225.4.52:3300/0,v1:10.225.4.52:6789/0] mon.las1
dumped monmap epoch 3
```

## CephFS

### Create

Create a CephFS volume:

```console
$ ceph fs volume create cephfs
```

List volumes:

```console
$ ceph fs volume ls
[
    {
        "name": "cephfs"
    }
]
```

The Ceph Orchestrator will automatically create and configure MDS for your file system, show the MDSes:

```console
$ ceph orch ps --daemon_type mds
NAME                    HOST  PORTS  STATUS        REFRESHED  AGE  MEM USE  MEM LIM  VERSION  IMAGE ID      CONTAINER ID  
mds.cephfs.las1.rfnkhk  las1         running (8m)     8m ago   8m    12.8M        -  19.2.3   af0c5903e901  5bd90f5152c2  
mds.cephfs.las3.roitqo  las3         running (8m)     8m ago   8m    12.9M        -  19.2.3   aade1b12b8e6  beaa5fb025d8
```

Show details about the new volume:

```console
$ ceph fs volume info cephfs
{
    "mon_addrs": [
        "10.225.4.54:6789",
        "10.225.4.53:6789",
        "10.225.4.52:6789"
    ],
    "pools": {
        "data": [
            {
                "avail": 20368515072,
                "name": "cephfs.cephfs.data",
                "used": 0
            }
        ],
        "metadata": [
            {
                "avail": 20368515072,
                "name": "cephfs.cephfs.meta",
                "used": 98304
            }
        ]
    }
}
```

Show all the pools:

```console
$ ceph osd pool ls
.mgr
cephfs.cephfs.meta
cephfs.cephfs.data
```

Note the name of data pool and metadata pool.

Create a subvolume group:

```console
$ ceph fs subvolumegroup create cephfs ceph-sg
```

Subvolume groups can have many policies appied, including a quota of capacity, file mode, file owner, etc.

Show subvolume groups in a volume:

```console
$ ceph fs subvolumegroup ls cephfs
[
    {
        "name": "ceph-sg"
    }
]
```

Get its path:

```console
$ ceph fs subvolumegroup getpath cephfs ceph-sg
/volumes/ceph-sg
```

Check if there are some subvolume groups in a volume:

```console
$ ceph fs subvolumegroup exist cephfs
subvolumegroup exists
```

Create a subvolume in a specified volume:

```console
$ ceph fs subvolume create cephfs ceph-vol --group-name ceph-sg
```

If `--group-name` is omitted, the subvolume would be put in a default group `_nogroup`.

List subvolumes in a volume:

```console
$ ceph fs subvolume ls cephfs ceph-sg
[
    {
        "name": "ceph-vol"
    }
]
```

If the subvolue is in the default group, the group name can be omitted.

Details of the subvolume:

```console
$ ceph fs subvolume info cephfs ceph-vol ceph-sg
{
    "atime": "2026-04-17 07:35:09",
    "bytes_pcent": "undefined",
    "bytes_quota": "infinite",
    "bytes_used": 0,
    "created_at": "2026-04-17 07:35:09",
    "ctime": "2026-04-17 07:35:09",
    "data_pool": "cephfs.cephfs.data",
    "earmark": "",
    "features": [
        "snapshot-clone",
        "snapshot-autoprotect",
        "snapshot-retention"
    ],
    "flavor": 2,
    "gid": 0,
    "mode": 16877,
    "mon_addrs": [
        "10.225.4.54:6789",
        "10.225.4.53:6789",
        "10.225.4.52:6789"
    ],
    "mtime": "2026-04-17 07:35:09",
    "path": "/volumes/ceph-sg/ceph-vol/8956fb8b-5a7c-48e7-a5fb-28ad8a0747c0",
    "pool_namespace": "",
    "state": "complete",
    "type": "subvolume",
    "uid": 0
}
```

:::{note}
The order of the parameters is `<volume-name> <subvolume-name> <group-name>`, or you can explicitly use `--group-name <group-name>`.
:::

Show the path of a subvolume:

```console
$ ceph fs subvolume getpath cephfs ceph-vol ceph-sg
/volumes/ceph-sg/ceph-vol/8956fb8b-5a7c-48e7-a5fb-28ad8a0747c0
```

### Mount

For we have `ceph.conf` and `ceph.client.admin.keyring` in directory `/etc/ceph/`, we can:

```console
$ sudo mkdir /mnt/cephfs
$ sudo mount -t ceph admin@.cephfs=/ /mnt/cephfs
$ ls /mnt/cephfs/
volumes
```

Generally, we do not want to expose `admin` credentials and want to restrict volume access. We can grant previlige to another client for this:

```console
$ ceph fs subvolume authorize cephfs ceph-vol --group-name ceph-sg xxxx
$ ceph fs subvolume authorized_list cephfs ceph-vol ceph-sg
[
    {
        "xxxx": "rw"
    }
]
```

where `xxxx` is the auth id.

:::{note}
`ceph fs subvolume authorize` grants subvolume access to an existing auth id. If the auth id does not exist yet, it only writes authorization metadata for the subvolume and does not create the CephX user.
:::

If you want to create a brand-new CephX user for one subvolume, it is clearer to use the subvolume path together with `ceph fs authorize`:

```console
$ sudo ceph fs authorize cephfs client.xxxx /volumes/ceph-sg/ceph-vol/8956fb8b-5a7c-48e7-a5fb-28ad8a0747c0 rw -o /etc/ceph/ceph.client.xxxx.keyring
```

:::{caution}
If there is a client with this name existing and its caps settings are exactly same as this command would set, the output will be nothing so clear the `keyring` file.
:::

Then the new user can be used to mount the subvolume:

```console
$ sudo mount -t ceph xxxx@.cephfs=/volumes/ceph-sg/ceph-vol/8956fb8b-5a7c-48e7-a5fb-28ad8a0747c0 /mnt/cephfs
```

If we do not want to expose the keyring file, we can create a file of the user's key and specify it in mount options:

```console
$ sudo rm /etc/ceph/ceph.client.xxxx.keyring
$ sudo ceph auth print-key client.xxxx > xxxx.secret
$ sudo mount -t ceph xxxx@.cephfs=/volumes/ceph-sg/ceph-vol/8956fb8b-5a7c-48e7-a5fb-28ad8a0747c0 /mnt/cephfs -o secretfile=xxxx.secret
```

The `mount` command complains that it cannot find keyring or key files in several places but the operation will succeed.

If the client machine does not have a usable `ceph.conf`, specify monitor addresses explicitly:

```console
$ sudo mount -t ceph xxxx@.cephfs=/volumes/ceph-sg/ceph-vol/8956fb8b-5a7c-48e7-a5fb-28ad8a0747c0 /mnt/cephfs -o mon_addr=10.225.4.52:6789/10.225.4.53:6789/10.225.4.54:6789,secret=AQCP8+Vpy4hhCRAA8/EZC8lIBE2c4rtdPRsq9g==
```

This time we use the key directly in the command line.

:::{tip}
The legacy format of this command is:

```console
$ sudo mount -t ceph 10.225.4.52:6789/10.225.4.53:6789/10.225.4.54:6789:/volumes/ceph-sg/ceph-vol/8956fb8b-5a7c-48e7-a5fb-28ad8a0747c0 /mnt/cephfs -o name=xxxx,secret=AQCP8+Vpy4hhCRAA8/EZC8lIBE2c4rtdPRsq9g==
```

:::

:::{caution}
The above command will leak the key via shell history. Do not use it.
:::

:::{hint}
For manual administration, `ceph fs authorize` is the simplest way to create a new user restricted to one subvolume path. If the CephX user already exists and you only need to add or change subvolume-level access, use `ceph fs subvolume authorize`.
:::

### Remove

Remove a volume is dangerous, so there is a config to control this:

```console
$ ceph config set mon mon_allow_pool_delete true
$ ceph config get mon mon_allow_pool_delete
true
```

Now you can delete a volume:

```console
$ ceph fs volume rm cephfs --yes-i-really-mean-it
metadata pool: cephfs.cephfs.meta data pool: ['cephfs.cephfs.data'] removed
```
