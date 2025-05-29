# csi-driver-nfs

## Install

Add and update the `helm` repository:

```console
$ helm repo add csi-driver-nfs https://raw.githubusercontent.com/kubernetes-csi/csi-driver-nfs/master/charts
"csi-driver-nfs" has been added to your repositories
$ helm repo update
```

Pull and install:

```console
$ helm pull csi-driver-nfs/csi-driver-nfs --version 4.11.0
$ helm install csi-driver-nfs csi-driver-nfs-4.11.0.tgz --namespace kube-system
NAME: csi-driver-nfs
LAST DEPLOYED: Wed May 14 18:23:45 2025
NAMESPACE: kube-system
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
The CSI NFS Driver is getting deployed to your cluster.

To check CSI NFS Driver pods status, please run:

  kubectl --namespace=kube-system get pods --selector="app.kubernetes.io/instance=csi-driver-nfs" --watch
```

## Usage

Create file `standard_sc.yaml` for a `StorageClass`:

:::{literalinclude} /_files/macos/workspace/k8s/standard_sc.yaml
:::

:::{note}
This class is set as default in the cluster.
:::

Apply to the cluster:

```console
$ kubectl apply -f standard_sc.yaml 
storageclass.storage.k8s.io/standard created
```
