# local-path-provisioner

<https://github.com/rancher/local-path-provisioner>

## Install

Download the definitions:

```console
$ curl -Lo local-path-storage-v0.0.37.yaml https://raw.githubusercontent.com/rancher/local-path-provisioner/v0.0.37/deploy/local-path-storage.yaml
```

Install it:

```console
$ kubectl apply -f local-path-storage-v0.0.37.yaml
namespace/local-path-storage created
serviceaccount/local-path-provisioner-service-account created
role.rbac.authorization.k8s.io/local-path-provisioner-role created
clusterrole.rbac.authorization.k8s.io/local-path-provisioner-role created
rolebinding.rbac.authorization.k8s.io/local-path-provisioner-bind created
clusterrolebinding.rbac.authorization.k8s.io/local-path-provisioner-bind created
deployment.apps/local-path-provisioner created
storageclass.storage.k8s.io/local-path created
configmap/local-path-config created
```

Show the StorageClass created:

```console
$ kubectl get sc
NAME         PROVISIONER             RECLAIMPOLICY   VOLUMEBINDINGMODE      ALLOWVOLUMEEXPANSION   AGE
local-path   rancher.io/local-path   Delete          WaitForFirstConsumer   false                  37s
```

If you want to make it the default:

```console
$ kubectl annotate sc local-path storageclass.kubernetes.io/is-default-class=true
storageclass.storage.k8s.io/local-path annotated
```

Done!
