# etcd

<https://etcd.io/>

## Install etcd client

::::{tab-set}
:::{tab-item} Ubuntu 22.04

By `snap`:

```console
$ sudo snap install etcd
etcd 3.4.36 from Canonical✓ installed
```

```console
$ which etcdctl
/snap/bin/etcdctl
$ etcdctl version
etcdctl version: 3.4.36
API version: 3.4
```

:::
::::

Install by downloading package binaries:

```console
$ curl -LO https://github.com/etcd-io/etcd/releases/download/v3.5.21/etcd-v3.5.21-linux-amd64.tar.gz
$ tar -xzf etcd-v3.5.21-linux-amd64.tar.gz
```

Install `etcd` client:

```console
$ sudo cp etcd-v3.5.21-linux-amd64/etcdctl /usr/local/bin
$ etcdctl version
etcdctl version: 3.5.21
API version: 3.5
```

## Access kubernetes' etcd

You need an `etcdctl` command of version matching your kubernetes' etcd. You can dig out the information in the output of:

```console
$ kubectl describe po -n kube-system -lcomponent=etcd
```

For the output, you can also get the details of certificates path.

Kubernetes secures `etcd` with TLS. Usually, the certificates and endpoint details are in your control plane node, often at:

- `/etc/kubernetes/pki/etcd/ca.crt` (CA cert)
- `/etc/kubernetes/pki/etcd/server.crt` (client cert)
- `/etc/kubernetes/pki/etcd/server.key` (client key)

The default endpoint is commonly `https://127.0.0.1:2379` if you’re on the control plane node. You can specify it in `etcdctl` command by parameter `--endpoints=`.

For these files are owned by `root`, you should run `etcdctl` as `root`.

Set the environment variables (adjust paths and endpoint if needed):

```sh
export ETCDCTL_API=3
export ETCDCTL_CACERT=/etc/kubernetes/pki/etcd/ca.crt
export ETCDCTL_CERT=/etc/kubernetes/pki/etcd/server.crt
export ETCDCTL_KEY=/etc/kubernetes/pki/etcd/server.key
```

Then run `etcdctl` command. For example, to list all keys:

```console
$ etcdctl get / --prefix --keys-only
```

Get a specific key:

```console
$ etcdctl get /registry/namespaces/default
```

The output is protobuf-encoded.
