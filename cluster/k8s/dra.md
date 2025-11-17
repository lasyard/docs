# Dynamic Resource Allocation

相关知识请参阅 Kubernetes 官网文档 <https://kubernetes.io/docs/concepts/scheduling-eviction/dynamic-resource-allocation/>, 目前是 1.34 版本。

## Kubernetes 1.32

请参阅 Kubernetes 官网文档 <https://v1-32.docs.kubernetes.io/docs/concepts/scheduling-eviction/dynamic-resource-allocation/>.

`DynamicResourceAllocation` 在 Kubernetes 1.32 上为 beta 特性，需要额外参数启用。如果集群是用 `kubeadm` 安装的，控制平面运行在 Pod 里，可用以下命令检查：

```console
$ kubectl get po -n kube-system -l tier=control-plane
NAME                           READY   STATUS    RESTARTS      AGE
etcd-las0                      1/1     Running   3 (23d ago)   177d
kube-apiserver-las0            1/1     Running   0             23h
kube-controller-manager-las0   1/1     Running   1 (23h ago)   23h
kube-scheduler-las0            1/1     Running   0             23h
```

这种情况下，需要在所有控制平面节点上修改以下三个文件：

1. `/etc/kubernetes/manifests/kube-apiserver.yaml`

   :::{literalinclude} /_files/ubuntu/etc/kubernetes/manifests/kube-apiserver.yaml
   :diff: /_files/ubuntu/etc/kubernetes/manifests/kube-apiserver.yaml.orig
   :::

2. `/etc/kubernetes/manifests/kube-controller-manager.yaml`

   :::{literalinclude} /_files/ubuntu/etc/kubernetes/manifests/kube-controller-manager.yaml
   :diff: /_files/ubuntu/etc/kubernetes/manifests/kube-controller-manager.yaml.orig
   :::

3. `/etc/kubernetes/manifests/kube-scheduler.yaml`

   :::{literalinclude} /_files/ubuntu/etc/kubernetes/manifests/kube-scheduler.yaml
   :diff: /_files/ubuntu/etc/kubernetes/manifests/kube-scheduler.yaml.orig
   :::

修改完成后相关的 Pod 会自动重启。

### 安装 dra-example-driver

`dra-example-driver` 是一个 DRA 设备驱动的 DEMO.

下载源码：

```console
$ git clone git@github.com:kubernetes-sigs/dra-example-driver.git
```

构建驱动（使用 docker 需要设置环境变量）

```console
$ cd dra-example-driver/
$ CONTAINER_TOOL=docker ./demo/build-driver.sh
```

使用 `helm` 部署到集群：

```console
$ helm upgrade -i --create-namespace --namespace dra-example-driver dra-example-driver deployments/helm/dra-example-driver
Release "dra-example-driver" does not exist. Installing it now.
NAME: dra-example-driver
LAST DEPLOYED: Tue Nov  4 17:45:05 2025
NAMESPACE: dra-example-driver
STATUS: deployed
REVISION: 1
TEST SUITE: None
```

查看其 Workloads:

```console
$ kubectl get all -n dra-example-driver
NAME                                         READY   STATUS    RESTARTS   AGE
pod/dra-example-driver-kubeletplugin-67x59   1/1     Running   0          3m53s
pod/dra-example-driver-kubeletplugin-j2bl2   1/1     Running   0          3m53s
pod/dra-example-driver-kubeletplugin-ndsw9   1/1     Running   0          3m53s

NAME                                              DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR   AGE
daemonset.apps/dra-example-driver-kubeletplugin   3         3         3       3            3           <none>          3m53s
```

查看生成的 ResourcesSlices 和 DeviceClasses:

```console
$ kubectl get resourceslice
NAME                         NODE   DRIVER            POOL   AGE
las1-gpu.example.com-n297b   las1   gpu.example.com   las1   4m8s
las2-gpu.example.com-tpwcb   las2   gpu.example.com   las2   4m18s
las3-gpu.example.com-m4zn4   las3   gpu.example.com   las3   4m22s
$ kubectl get deviceclasses
NAME              AGE
gpu.example.com   7m39s
```

进一步查看 ResourceSlice 的说明：

```console
$ kdesc resourceslice las1-gpu.example.com-n297b
Name:         las1-gpu.example.com-n297b
Namespace:
Labels:       <none>
Annotations:  <none>
API Version:  resource.k8s.io/v1beta1
Kind:         ResourceSlice
...
Spec:
  Devices:
    Basic:
      Attributes:
        Driver Version:
          Version:  1.0.0
        Index:
          Int:  0
        Model:
          String:  LATEST-GPU-MODEL
        Uuid:
          String:  gpu-94011f0b-8dcd-b4b0-cd99-40eab2e3c96a
      Capacity:
        Memory:
          Value:  80Gi
    Name:         gpu-0
...
```

可以看到生成了名为 `gpu-*` 的设备（实际上每个节点上有 8 个）。

:::{note}
驱动卸载时没有删除 ResourceSlices. 用以下命令删除：

```console
$ kubectl delete resourceslice --field-selector spec.driver=gpu.example.com
resourceslice.resource.k8s.io "las1-gpu.example.com-n297b" deleted
resourceslice.resource.k8s.io "las2-gpu.example.com-tpwcb" deleted
resourceslice.resource.k8s.io "las3-gpu.example.com-m4zn4" deleted
```

:::

### 测试

在集群内创建一个 ResourceClaimTemplate:

```console
$ kubectl apply -f example_resourceclaimtemplate.yaml 
resourceclaimtemplate.resource.k8s.io/example created
```

其定义如下：

:::{literalinclude} /_files/macos/workspace/k8s/dra/example_resourceclaimtemplate.yaml
:::

再创建一个 Pod 进行测试。Pod 的定义如下：

:::{literalinclude} /_files/macos/workspace/k8s/dra/example_claim_po.yaml
:::

创建 Pod 时可以监视 ResourceClaim 资源的变化：

```console
$ kubectl get resourceclaim -w
NAME                          STATE     AGE
example-claim-example-4cb2t   pending   0s
example-claim-example-4cb2t   pending   0s
example-claim-example-4cb2t   allocated,reserved   0s
example-claim-example-4cb2t   pending              63s
example-claim-example-4cb2t   pending              63s
example-claim-example-4cb2t   pending              63s
```

这种自动生成的 ResourceClaim 的所有者是这个 Pod, 当 Pod 被删除时它也被删除。

## Kubernetes 1.34

把集群升级到 1.34:

```console
$ kubectl get no
NAME   STATUS   ROLES           AGE    VERSION
las0   Ready    control-plane   189d   v1.34.2
las1   Ready    <none>          189d   v1.34.2
las2   Ready    <none>          189d   v1.34.2
las3   Ready    <none>          185d   v1.34.2
```

`DynamicResourceAllocation` 特性在 Kubernetes 1.34 上默认启用，所以之前的额外参数可以去掉，但别忘了升级服务映像的版本：

1. `/etc/kubernetes/manifests/kube-apiserver.yaml`

   :::{literalinclude} /_files/ubuntu/etc/kubernetes/manifests/kube-apiserver_1.34.yaml
   :diff: /_files/ubuntu/etc/kubernetes/manifests/kube-apiserver.yaml.orig
   :::

2. `/etc/kubernetes/manifests/kube-controller-manager.yaml`

   :::{literalinclude} /_files/ubuntu/etc/kubernetes/manifests/kube-controller-manager_1.34.yaml
   :diff: /_files/ubuntu/etc/kubernetes/manifests/kube-controller-manager.yaml.orig
   :::

3. `/etc/kubernetes/manifests/kube-scheduler.yaml`

   :::{literalinclude} /_files/ubuntu/etc/kubernetes/manifests/kube-scheduler_1.34.yaml
   :diff: /_files/ubuntu/etc/kubernetes/manifests/kube-scheduler.yaml.orig
   :::

检查 API 版本以确认：

```console
$ kubectl api-versions | grep resource.k8s.io
resource.k8s.io/v1
```

重新安装 dra-example-driver.

ResourceClaimTemplate 需要修改：

:::{literalinclude} /_files/macos/workspace/k8s/dra/example_resourceclaimtemplate_1.34.yaml
:diff: /_files/macos/workspace/k8s/dra/example_resourceclaimtemplate.yaml
:::

原来的对应字段被挪到了 `exactly` 下面。`exactly` 可以变为 `firstAvailable`, 其下可以放置一个列表以提供备选。

Pod 的定义不需要任何修改。
