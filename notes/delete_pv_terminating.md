# 删除无法终止的 PV

## 问题

在 Kubernetes 集群中删除一个 PV 时，PV 一直处于 `Terminating` 无法删除。

## 分析

通常是因为 PV 的 Finalizer 阻止了 PV 被删除。使用以下命令查看 PV 的 Finalizer:

```console
$ kubectl get pv pv-xxxx -ojsonpath --template {.metadata.finalizers} | jq
[
  "external-provisioner.volume.kubernetes.io/finalizer",
  "kubernetes.io/pv-protection"
]
```

## 解决方案

删除 PV 的 Finalizer:

```console
$ kubectl patch pv pv-xxxx -p '{"metadata":{"finalizers":null}}'
persistentvolume/pvc-a7abf83d-baef-4aa6-9418-3beed827c5d6 patched
```
