# ceph-csi-cephfs

## Prerequiste

CephFS CSI need a SubvolumeGroup to create volumes for kubernetes. So make one in ceph cluster:

```console
$ ceph fs subvolumegroup create cephfs csi
$ ceph fs authorize cephfs client.csi /volumes/csi rw
[client.csi]
    key = AQDe6epp9PNxNhAAxNMCkbqfwUzfhSu9+rsmdg==
    caps mds = "allow rw fsname=cephfs path=/volumes/csi"
    caps mon = "allow r fsname=cephfs"
    caps osd = "allow rw tag cephfs data=cephfs"
```

A client `csi` is created for this purpose. But, the driver want to create Subvolumes in this SubvolumeGroup, thus the caps above are not enough. Modify the caps for this client as:

```console
$ ceph auth caps client.csi mon "allow r fsname=cephfs" mgr "allow rw" mds "allow rw fsname=cephfs path=/volumes/csi" osd "allow rw tag cephfs *=cephfs"
```

Two points:

- `rw` access to `mgr`
- `rw` access to `osd` file system `cephfs` not only `data` pool but also `meta` pool

## Install

Download helm charts:

```console
$ helm repo add ceph-csi https://ceph.github.io/csi-charts/
"ceph-csi" has been added to your repositories
$ helm repo update
...
$ helm pull ceph-csi/ceph-csi-cephfs
```

Write a `ceph_csi_cephfs_values.yaml` file:

:::{literalinclude} /_files/macos/workspace/k8s/ceph_csi_cephfs_values.yaml
:::

Install:

```console
$ helm install ceph-csi-cephfs ceph-csi-cephfs-3.16.2.tgz -n ceph-csi-cephfs --create-namespace -f ceph_csi_cephfs_values.yaml
NAME: ceph-csi-cephfs
LAST DEPLOYED: Fri Apr 24 10:16:57 2026
NAMESPACE: ceph-csi-cephfs
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
Examples on how to configure a storage class and start using the driver are here:
https://github.com/ceph/ceph-csi/tree/v3.16.2/examples/cephfs
```

Show installed workloads:

```console
$ kubectl get all -n ceph-csi-cephfs
NAME                                               READY   STATUS    RESTARTS   AGE
pod/ceph-csi-cephfs-nodeplugin-s5m52               3/3     Running   0          116s
pod/ceph-csi-cephfs-nodeplugin-tb7dj               3/3     Running   0          116s
pod/ceph-csi-cephfs-nodeplugin-w8vh4               3/3     Running   0          116s
pod/ceph-csi-cephfs-provisioner-849d8678c5-5s78c   6/6     Running   0          116s
pod/ceph-csi-cephfs-provisioner-849d8678c5-8t6pf   6/6     Running   0          116s
pod/ceph-csi-cephfs-provisioner-849d8678c5-vfvlc   6/6     Running   0          116s

NAME                                               TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)    AGE
service/ceph-csi-cephfs-nodeplugin-http-metrics    ClusterIP   10.105.40.236    <none>        8080/TCP   116s
service/ceph-csi-cephfs-provisioner-http-metrics   ClusterIP   10.105.146.166   <none>        8080/TCP   116s

NAME                                        DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR   AGE
daemonset.apps/ceph-csi-cephfs-nodeplugin   3         3         3       3            3           <none>          116s

NAME                                          READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/ceph-csi-cephfs-provisioner   3/3     3            3           116s

NAME                                                     DESIRED   CURRENT   READY   AGE
replicaset.apps/ceph-csi-cephfs-provisioner-849d8678c5   3         3         3       116s
```

Related ConfigMaps:

```console
$ kubectl get cm -n ceph-csi-cephfs
NAME                             DATA   AGE
ceph-config                      2      3m3s
ceph-csi-config                  1      3m3s
ceph-csi-encryption-kms-config   1      3m3s
kube-root-ca.crt                 1      3d15h
```

The ceph cluster config is in `ceph-csi-config`.

Created StorageClass:

```console
$ kubectl get sc
NAME            PROVISIONER           RECLAIMPOLICY   VOLUMEBINDINGMODE   ALLOWVOLUMEEXPANSION   AGE
csi-cephfs-sc   cephfs.csi.ceph.com   Delete          Immediate           true                   5m
```

Ceph client credentials:

```console
$ kubectl get secret -n ceph-csi-cephfs
NAME                                    TYPE                 DATA   AGE
csi-cephfs-secret                       Opaque               2      8m33s
sh.helm.release.v1.ceph-csi-cephfs.v1   helm.sh/release.v1   1      8m33s
```

The `userID` and `userKey` in `csi-cephfs-secret` is only BASE64 coded:

```console
$ kubectl get secret csi-cephfs-secret -n ceph-csi-cephfs -ojsonpath='{.data.userID}' | base64 --decode
csi
```

:::{tip}
We can restore the information needed to mount a CephFS volume if we can touch the ceph CSI driver in kubernetes.
:::

## Allocate PVs

### Dynamic

By specify `spec.storageClassName` in a `pvc`, the underlying `pv` can be automatically provisioned. For example, create a `pvc` and Pod as:

:::{literalinclude} /_files/macos/workspace/k8s/dynamic_ceph_pv_po.yaml
:::

Show the `pvc` and created `pv`, dig out the volume path of the `pv`:

```console
$ kubectl get pvc csi-cephfs-pvc
NAME             STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS    VOLUMEATTRIBUTESCLASS   AGE
csi-cephfs-pvc   Bound    pvc-acacc432-af06-484d-9f32-fca65d7616e1   1Gi        RWX            csi-cephfs-sc   <unset>                 32s
$ kubectl get pv pvc-acacc432-af06-484d-9f32-fca65d7616e1
NAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                            STORAGECLASS    VOLUMEATTRIBUTESCLASS   REASON   AGE
pvc-acacc432-af06-484d-9f32-fca65d7616e1   1Gi        RWX            Delete           Bound    ceph-csi-cephfs/csi-cephfs-pvc   csi-cephfs-sc   <unset>                          63s
$ kubectl get pv pvc-acacc432-af06-484d-9f32-fca65d7616e1 -ojsonpath='{.spec.csi.volumeAttributes.subvolumePath}'
/volumes/csi/csi-vol-7d79a879-0a14-49c9-bfab-0637e5360111/89053c31-1ad3-4f94-8df6-395afcb8b838
```

Show the create subvolue in ceph:

```console
$ ceph fs subvolume ls cephfs csi
[
    {
        "name": "csi-vol-7d79a879-0a14-49c9-bfab-0637e5360111"
    }
]
$ ceph fs subvolume getpath cephfs csi-vol-7d79a879-0a14-49c9-bfab-0637e5360111 csi
/volumes/csi/csi-vol-7d79a879-0a14-49c9-bfab-0637e5360111/89053c31-1ad3-4f94-8df6-395afcb8b838
```

If the volumes is mounted on somewhere else, you can see a `.meta` file in the directory of subvolume:

```console
$ sudo cat .meta
[GLOBAL]
version = 2
type = subvolume
path = /volumes/csi/csi-vol-7d79a879-0a14-49c9-bfab-0637e5360111/89053c31-1ad3-4f94-8df6-395afcb8b838
state = complete

[USER_METADATA]
csi.storage.k8s.io/pvc/name = csi-cephfs-pvc
csi.storage.k8s.io/pvc/namespace = ceph-csi-cephfs
csi.storage.k8s.io/pv/name = pvc-acacc432-af06-484d-9f32-fca65d7616e1
.cephfs.csi.ceph.com/userid/0001-0024-990b5070-3964-11f1-8888-476de7d3e05c-0000000000000003-7d79a879-0a14-49c9-bfab-0637e5360111/las1 = csi
```

This file cannot be found in the pod, because where the pod used is a subdirectory in this directory.

Dynamically provisioned `pv` will be deleted after released.

### Static

Static `pv` need a dedicated subvolume in CephFS, create one:

```console
$ ceph fs subvolume create cephfs static_vol csi
```

Authorize to a new client:

```console
$ ceph fs subvolume authorize cephfs static_vol --group-name csi csi-static
```

This create a new client `csi-static`. Get its credentials:

```console
$ ceph auth get client.csi-static
[client.csi-static]
    key = AQACJetpyvjeDBAAvHBRzZEaGgE4UKhoJLN1Hg==
    caps mds = "allow rw path=/volumes/csi/static_vol/26d36559-7994-47b5-9bde-78ec34486754"
    caps mon = "allow r"
    caps osd = "allow rw pool=cephfs.cephfs.data"
```

Now create the `pv` (also with a Secret to provide credentials for user `csi-static`):

:::{literalinclude} /_files/macos/workspace/k8s/cephfs_static_pv.yaml
:::

The `userID` and `userKey` here are plaintext and Kubernetes will `base64` encode it and move to `data` field.

Then the `pvc` and Pod (show the diff from the dynamic one):

:::{literalinclude} /_files/macos/workspace/k8s/static_ceph_pv_po.yaml
:diff: /_files/macos/workspace/k8s/dynamic_ceph_pv_po.yaml
:::

:::{note}
We do not need a StorageClass for this, so the empty string is needed here. Because if it is ommited, the default StorageClass will be used if there is.
:::

After delete the Pod, show the status of the `pv`:

```console
$ kubectl get pv csi-static-pv
NAME            CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS     CLAIM                    STORAGECLASS   VOLUMEATTRIBUTESCLASS   REASON   AGE
csi-static-pv   1Gi        RWX            Retain           Released   default/csi-cephfs-pvc                  <unset>                          8m9s
```

The `pv` is kept, but cannot be re-mount to another Pod because its status is `Released`. You must make it `Available` to use again:

```console
$ kubectl patch pv csi-static-pv --type=json -p='[{"op":"remove","path":"/spec/claimRef"}]'
persistentvolume/csi-static-pv patched
$ kubectl get pv csi-static-pv                                                                   
NAME            CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS      CLAIM   STORAGECLASS   VOLUMEATTRIBUTESCLASS   REASON   AGE
csi-static-pv   1Gi        RWX            Retain           Available                          <unset>                          11m
```
