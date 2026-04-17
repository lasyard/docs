# cephadm

<https://docs.ceph.com/en/latest/cephadm>

`cephadm` is a utility that is used to manage a ceph cluster. It doesn't rely on the credentials to access the ceph cluster, or a running `mon` daemon, but must be run as `root`. In case of `ceph` command cannot access the cluster, it can save us.

## Deamons management

Use `sudo cephadm ls` to list ceph deamons run on this host (the output is in JSON format), for example:

```console
$ sudo cephadm ls | jq -r '.[].name'
mon.las3
mgr.las3.svwbki
grafana.las3
alertmanager.las3
crash.las3
ceph-exporter.las3
prometheus.las3
```

The above command list names of the daemons.

`cephadm` can enable a ceph service like `systemctl` does:

```console
$ sudo cephadm unit enable -n mon.las3 --fsid 628d3140-37c9-11f1-8f6f-d3e73c698443
Inferring config /var/lib/ceph/628d3140-37c9-11f1-8f6f-d3e73c698443/mon.las3/config
stderr Created symlink /etc/systemd/system/ceph-628d3140-37c9-11f1-8f6f-d3e73c698443.target.wants/ceph-628d3140-37c9-11f1-8f6f-d3e73c698443@mon.las3.service → /etc/systemd/system/ceph-628d3140-37c9-11f1-8f6f-d3e73c698443@.service.
```

Restart the service:

```console
$ sudo cephadm unit restart -n mon.las3 --fsid 628d3140-37c9-11f1-8f6f-d3e73c698443
Inferring config /var/lib/ceph/628d3140-37c9-11f1-8f6f-d3e73c698443/mon.las3/config
```

:::{important}
Do not manage ceph services by `systemctl` if your cluster is managed by `cephadm`, the ceph orchestrator is guarding these settings.
:::

## Enable a shell

```console
$ sudo cephadm shell
Inferring fsid 628d3140-37c9-11f1-8f6f-d3e73c698443
Inferring config /var/lib/ceph/628d3140-37c9-11f1-8f6f-d3e73c698443/mon.las3/config
Using ceph image with id 'aade1b12b8e6' and tag 'v19' created on 2025-07-18 03:53:27 +0800 CST
quay.io/ceph/ceph@sha256:af0c5903e901e329adabe219dfc8d0c3efc1f05102a753902f33ee16c26b6cee
root@las3:/#
```

You can also specify the `fsid`:

```console
$ sudo cephadm shell --fsid 628d3140-37c9-11f1-8f6f-d3e73c698443
```

By default, the shell is opened on mon daemon container, you can specify it using `--name` or `-n`:

```console
$ sudo cephadm shell -n mgr.las3.svwbki
Inferring fsid 628d3140-37c9-11f1-8f6f-d3e73c698443
Inferring config /var/lib/ceph/628d3140-37c9-11f1-8f6f-d3e73c698443/mgr.las3.svwbki/config
...
```

## Destroy a cluster

The following command can destroy the cluster installed by `cephadm` on a node:

```console
$ sudo cephadm rm-cluster --force --zap-osds --fsid $(ceph fsid)
Deleting cluster with fsid: 628d3140-37c9-11f1-8f6f-d3e73c698443
...
```
