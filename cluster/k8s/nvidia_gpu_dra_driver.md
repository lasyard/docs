# Nvidia GPU DRA Driver

:::{note}
这个驱动将来可能被整合进 GPU Operator.
:::

## 安装

首先必须在主机上安装 Nvidia driver, 并且版本要求最低为 570.158.01. 这里安装的是 `cuda_13.0.0_580.65.06_linux`.

然后需要[安装 GPU Operator](project:nvidia_gpu_operator.md). 因为主机已经安装了驱动，所以要指定 `--set driver.enabled=false`. 这里安装的是 `v25.10.0`.

用 `helm` 安装 nvidia-dra-driver-gpu:

```console
$ helm pull nvidia/nvidia-dra-driver-gpu --create-namespace
$ helm install nvidia-dra-driver-gpu nvidia-dra-driver-gpu-25.8.0.tgz --create-namespace --namespace nvidia-dra-driver-gpu --set resources.gpus.enabled=true --set gpuResourcesEnabledOverride=true
NAME: nvidia-dra-driver-gpu
LAST DEPLOYED: Tue Nov 18 17:02:44 2025
NAMESPACE: nvidia-dra-driver-gpu
STATUS: deployed
REVISION: 1
TEST SUITE: None
```

GPU 资源默认是关闭的，如果一定要打开，需要同时设置 `--set gpuResourcesEnabledOverride=true`.

查看安装后的 Workloads:

```console
$ kubectl get all -owide -n nvidia-dra-driver-gpu
NAME                                                   READY   STATUS    RESTARTS   AGE   IP                NODE   NOMINATED NODE   READINESS GATES
pod/nvidia-dra-driver-gpu-controller-b94fd47b6-tn562   1/1     Running   0          27s   192.168.100.169   las0   <none>           <none>
pod/nvidia-dra-driver-gpu-kubelet-plugin-7wnc5         2/2     Running   0          27s   192.168.185.45    las3   <none>           <none>

NAME                                                  DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR   AGE   CONTAINERS             IMAGES                                                                                SELECTOR
daemonset.apps/nvidia-dra-driver-gpu-kubelet-plugin   1         1         1       1            1           <none>          27s   compute-domains,gpus   nvcr.io/nvidia/k8s-dra-driver-gpu:v25.8.0,nvcr.io/nvidia/k8s-dra-driver-gpu:v25.8.0   nvidia-dra-driver-gpu-component=kubelet-plugin

NAME                                               READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS       IMAGES                                      SELECTOR
deployment.apps/nvidia-dra-driver-gpu-controller   1/1     1            1           27s   compute-domain   nvcr.io/nvidia/k8s-dra-driver-gpu:v25.8.0   nvidia-dra-driver-gpu-component=controller

NAME                                                         DESIRED   CURRENT   READY   AGE   CONTAINERS       IMAGES                                      SELECTOR
replicaset.apps/nvidia-dra-driver-gpu-controller-b94fd47b6   1         1         1       27s   compute-domain   nvcr.io/nvidia/k8s-dra-driver-gpu:v25.8.0   nvidia-dra-driver-gpu-component=controller,pod-template-hash=b94fd47b6
```

注意 kubelet plugin 只在 GPU 节点上运行，controller 在控制平面节点上运行。

查看安装的 DeviceClasses:

```console
$ kubectl get deviceclass
NAME                                        AGE
compute-domain-daemon.nvidia.com            82s
compute-domain-default-channel.nvidia.com   82s
gpu.nvidia.com                              82s
mig.nvidia.com                              82s
```

查看生成的 ResourceSlices:

```console
$ kubectl get resourceslice
NAME                                   NODE   DRIVER                      POOL   AGE
las3-compute-domain.nvidia.com-ws7tv   las3   compute-domain.nvidia.com   las3   100s
las3-gpu.nvidia.com-trjfv              las3   gpu.nvidia.com              las3   100s
```

查看 GPU resource 的详情：

```console
$ kubectl describe resourceslice las3-gpu.nvidia.com-trjfv 
Name:         las3-gpu.nvidia.com-trjfv
Namespace:    
Labels:       <none>
Annotations:  <none>
API Version:  resource.k8s.io/v1
Kind:         ResourceSlice
...
Spec:
  Devices:
    Attributes:
      Architecture:
        String:  Pascal
      Brand:
        String:  Tesla
      Cuda Compute Capability:
        Version:  6.1.0
      Cuda Driver Version:
        Version:  13.0.0
      Driver Version:
        Version:  580.65.6
      Pcie Bus ID:
        String:  0000:00:05.0
      Product Name:
        String:  Tesla P4
      resource.kubernetes.io/pcieRoot:
        String:  pci0000:00
      Type:
        String:  gpu
      Uuid:
        String:  GPU-1183b79f-301d-9b3f-a0b7-09ee1b54be60
    Capacity:
      Memory:
        Value:  7680Mi
    Name:       gpu-0
  Driver:       gpu.nvidia.com
  Node Name:    las3
  Pool:
    Generation:            1
    Name:                  las3
    Resource Slice Count:  1
Events:                    <none>
```

可见 Device 的属性描述了 GPU 的各种参数。另外 ResourceSlice 是全局的，不分 Namespace.

## 测试

### 使用 ResourceClaimTemplate

创建一个 ResourceClaimTemplate:

:::{literalinclude} /_files/macos/workspace/k8s/dra/gpu_resourceclaimtemplate.yaml
:::

创建一个 Pod, 使用刚才的 ResourceClaimTemplate:

:::{literalinclude} /_files/macos/workspace/k8s/dra/gpu_po.yaml
:::

查看自动生成的 ResourceClaim:

```console
$ kubectl get resourceclaim 
NAME            STATE                AGE
gpu-gpu-c7f6x   allocated,reserved   2m34s
```

这个 ResourceClaim 会在 Pod 运行结束后（不是删除后）自动删除。

检查 Pod 中的 GPU:

```console
$ kubectl exec gpu -- nvidia-smi
Tue Nov 18 09:22:33 2025
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 580.65.06              Driver Version: 580.65.06      CUDA Version: 13.0     |
+-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  Tesla P4                       Off |   00000000:00:05.0 Off |                    0 |
| N/A   36C    P8              6W /   75W |       0MiB /   7680MiB |      0%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+

+-----------------------------------------------------------------------------------------+
| Processes:                                                                              |
|  GPU   GI   CI              PID   Type   Process name                        GPU Memory |
|        ID   ID                                                               Usage      |
|=========================================================================================|
|  No running processes found                                                             |
+-----------------------------------------------------------------------------------------+
```

### 使用 ResourceClaim

创建一个 ResourceClaim:

:::{literalinclude} /_files/macos/workspace/k8s/dra/gpu_resourceclaim.yaml
:::

创建一个 Job, 同时生成两个 Pod 使用刚才的 ResourceClaim:

:::{literalinclude} /_files/macos/workspace/k8s/dra/gpu_job.yaml
:::

容易验证两个 Pod 都能使用同一个 GPU.

另外如果监视 ResourceClaim 的状态，可以得到：

```console
$ kubectl get resourceclaim -w
NAME   STATE     AGE
gpu    pending   0s
gpu    pending   6s
gpu    allocated,reserved   6s
gpu    allocated,reserved   6s
gpu    allocated,reserved   69s
gpu    allocated,reserved   69s
gpu    allocated,reserved   69s
gpu    allocated,reserved   69s
gpu    allocated,reserved   69s
gpu    allocated,reserved   69s
gpu    allocated,reserved   69s
gpu    allocated,reserved   69s
gpu    allocated,reserved   69s
gpu    allocated,reserved   69s
gpu    allocated,reserved   69s
gpu    allocated,reserved   69s
gpu    allocated,reserved   69s
gpu    allocated,reserved   69s
gpu    allocated,reserved   69s
gpu    allocated,reserved   69s
gpu    allocated,reserved   69s
gpu    pending              69s
gpu    pending              69s
```
