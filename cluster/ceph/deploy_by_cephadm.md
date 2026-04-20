# Deploy Ceph By Cephadm

## Bootstrap a new cluster

`cephadm` uses docker to run services, so [install docker](project:/cluster/docker/install.md) first on each host.

Bootstrap a cluster:

```console
$ sudo cephadm bootstrap --mon-ip 10.225.4.54 --cluster-network 10.225.4.0/24
Verifying podman|docker is present...
Verifying lvm2 is present...
Verifying time synchronization is in place...
Unit systemd-timesyncd.service is enabled and running
Repeating the final host check...
docker (/usr/bin/docker) is present
systemctl is present
lvcreate is present
Unit systemd-timesyncd.service is enabled and running
Host looks OK
Cluster fsid: 990b5070-3964-11f1-8888-476de7d3e05c
Verifying IP 10.225.4.54 port 3300 ...
Verifying IP 10.225.4.54 port 6789 ...
...
Pulling container image quay.io/ceph/ceph:v19...
Ceph version: ceph version 19.2.3 (c92aebb279828e9c3c1f5d24613efca272649e62) squid (stable)
...
Ceph Dashboard is now available at:

         URL: https://las3:8443/
        User: admin
    Password: 5fr4ko9zq3

Enabling client.admin keyring and conf on hosts with "admin" label
Saving cluster configuration to /var/lib/ceph/990b5070-3964-11f1-8888-476de7d3e05c/config directory
You can access the Ceph CLI as following in case of multi-cluster or non-default config:

    sudo /usr/sbin/cephadm shell --fsid 990b5070-3964-11f1-8888-476de7d3e05c -c /etc/ceph/ceph.conf -k /etc/ceph/ceph.client.admin.keyring

Or, if you are only running a single cluster on this host:

    sudo /usr/sbin/cephadm shell 

Please consider enabling telemetry to help improve Ceph:

    ceph telemetry on

For more information see:

    https://docs.ceph.com/en/latest/mgr/telemetry/

Bootstrap complete.
```

The files created in directory `/etc/ceph` is not used by the ceph cluster deployed above, for they are running in containers, but for the `ceph` command on the host. Change the owner and permissions to make it available for the current user `ubuntu`:

```console
$ sudo chown ceph:ceph /etc/ceph/ceph.client.admin.keyring
$ sudo chmod g+r /etc/ceph/ceph.client.admin.keyring
$ sudo usermod -aG ceph ubuntu
```

Show the version using `ceph`:

```console
$ ceph version
ceph version 19.2.3 (c92aebb279828e9c3c1f5d24613efca272649e62) squid (stable)
```

For there are already node exporter deployed, we need to change the exporter port of ceph. Write a apply spec `node-exporter.yaml` as below:

:::{literalinclude} /_files/ubuntu/workspace/ceph/node-exporter.yaml
:::

Then apply it:

```console
$ ceph orch apply -i node-exporter-port.yaml 
Scheduled node-exporter update...
```

Show status of the ceph cluster:

```console
$ ceph status
  cluster:
    id:     990b5070-3964-11f1-8888-476de7d3e05c
    health: HEALTH_WARN
            OSD count 0 < osd_pool_default_size 3
 
  services:
    mon: 1 daemons, quorum las3 (age 109m)
    mgr: las3.aadzsn(active, since 107m)
    osd: 0 osds: 0 up, 0 in
 
  data:
    pools:   0 pools, 0 pgs
    objects: 0 objects, 0 B
    usage:   0 B used, 0 B / 0 B avail
    pgs:     

```

For now, status of the cluster is not healthy because the number of OSDs is 0.

### Add OSDs

Normally, ceph uses real disks as OSD storage. The following command list all available devices that can be used (not tested):

```console
$ ceph orch device ls
```

Then you can add them all as OSD (not tested):

```console
$ ceph orch apply osd --all-available-devices
```

For test purpose, we can create loop devices to service as OSD. But the command above cannot be applied. Need some low-level command to do this.

First, [create a loop device](project:/app/cli/losetup.md) with enough size. Check it:

```console
$ lsblk /dev/loop0
NAME  MAJ:MIN RM SIZE RO TYPE MOUNTPOINTS
loop0   7:0    0  20G  0 loop
```

Then [setup a logical volume](project:/app/cli/lvm.md) on the device (for ceph orchestrator do not allow loop devices), check it:

```console
$ sudo lvs
  LV         VG     Attr       LSize   Pool Origin Data%  Meta%  Move Log Cpy%Sync Convert
  ceph-osd-0 ceph-0 -wi-a----- <20.00g
```

The device file of it is `/dev/ceph-0/ceph-osd-0`. Add it as a OSD:

```console
$ ceph orch daemon add osd las3:/dev/ceph-0/ceph-osd-0
Created osd(s) 0 on host 'las3'
```

See the new created OSD:

```console
$ ceph osd ls
0
$ ceph osd tree
ID  CLASS  WEIGHT   TYPE NAME      STATUS  REWEIGHT  PRI-AFF
-1         0.01949  root default                            
-3         0.01949      host las3                           
 0    hdd  0.01949          osd.0      up   1.00000  1.00000
$ ceph osd crush tree
ID  CLASS  WEIGHT   TYPE NAME    
-1         0.01949  root default 
-3         0.01949      host las3
 0    hdd  0.01949          osd.0
$ ceph osd df
ID  CLASS  WEIGHT   REWEIGHT  SIZE    RAW USE  DATA    OMAP     META    AVAIL   %USE  VAR   PGS  STATUS
 0    hdd  0.01949   1.00000  20 GiB  426 MiB  80 KiB    1 KiB  26 MiB  20 GiB  2.08  1.00    0      up
                       TOTAL  20 GiB  426 MiB  80 KiB  1.6 KiB  26 MiB  20 GiB  2.08
MIN/MAX VAR: 1.00/1.00  STDDEV: 0
```

The information above shows that osd.0 is add to the CRUSH, so is ready to receive data. We still need to add 2 OSDs to make the cluster healthy.

### Add hosts

Now we want to add new hosts to the cluster. First, make sure `root` user can access the host password-free. The simplest way is copy `/etc/ceph/ceph.pub` to the new host's `/root/.ssh/authorized_keys` file. Also `ceph` command must be installed on the target hosts.

```console
$ ceph orch host add las2 10.225.4.53
Added host 'las2' with addr '10.225.4.53'
```

:::{important}
Best providing the ip, for there may be many ips for the host and the auto resolved one may not be appropriate.
:::

Now follow the same process on `las1` to create logical volume, and add an OSD located in the new host:

```console
$ ceph orch daemon add osd las2:/dev/ceph-0/ceph-osd-0
Created osd(s) 1 on host 'las2'
```

Add another host and OSD and the cluster finally have 3 OSDs, which is healthy:

```console
$ ceph status
  cluster:
    id:     990b5070-3964-11f1-8888-476de7d3e05c
    health: HEALTH_OK
 
  services:
    mon: 3 daemons, quorum las3,las2,las1 (age 16h)
    mgr: las3.aadzsn(active, since 20h), standbys: las2.zwklfj
    osd: 3 osds: 3 up (since 16h), 3 in (since 16h)
 
  data:
    pools:   1 pools, 1 pgs
    objects: 2 objects, 449 KiB
    usage:   81 MiB used, 60 GiB / 60 GiB avail
    pgs:     1 active+clean
```

Now the `/etc/ceph/ceph.conf` looks like:

:::{literalinclude} /_files/ubuntu/etc/ceph/ceph.conf
:::
