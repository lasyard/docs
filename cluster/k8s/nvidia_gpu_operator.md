# NVIDIA GPU Operator

Add repository:

```console
$ helm repo add nvidia https://helm.ngc.nvidia.com/nvidia
"nvidia" has been added to your repositories
```

Install:

```console
$ helm pull nvidia/gpu-operator --version=v25.3.2
$ helm install gpu-operator -n gpu-operator --create-namespace gpu-operator-v25.3.2.tgz --set driver.enabled=false
W0828 11:26:49.734907   75972 warnings.go:70] spec.template.spec.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[0].preference.matchExpressions[0].key: node-role.kubernetes.io/master is use "node-role.kubernetes.io/control-plane" instead
W0828 11:26:49.734838   75972 warnings.go:70] spec.template.spec.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[0].preference.matchExpressions[0].key: node-role.kubernetes.io/master is use "node-role.kubernetes.io/control-plane" instead
W0828 11:26:49.755071   75972 warnings.go:70] unknown field "spec.dcgmExporter.service"
NAME: gpu-operator
LAST DEPLOYED: Thu Aug 28 11:26:49 2025
NAMESPACE: gpu-operator
STATUS: deployed
REVISION: 1
TEST SUITE: None
```

:::{note}
Nvidia driver is already installed on the gpu node, that is why `driver.enabled=false` is set.

If some pods of gpu-operator report error: "failed to get sandbox runtime: no runtime for "nvidia" is configured", you may need to config `containerd` by (generally the operator do this for you):

```console
$ sudo nvidia-ctk runtime configure --runtime=containerd
INFO[0000] Using config version 2                       
INFO[0000] Using CRI runtime plugin name "io.containerd.grpc.v1.cri" 
INFO[0000] Wrote updated config to /etc/containerd/config.toml 
INFO[0000] It is recommended that containerd daemon be restarted.
$ sudo systemctl restart containerd
```

:::

Now see the gpu node:

```console
$ kubectl describe no las3
...
Capacity:
  cpu:                8
  ephemeral-storage:  203056560Ki
  hugepages-1Gi:      0
  hugepages-2Mi:      0
  memory:             8125876Ki
  nvidia.com/gpu:     1
  pods:               110
...
```

Create a pod config file `gpu_po.yaml`:

:::{literalinclude} /_files/macos/workspace/k8s/gpu_po.yaml
:::

Apply to the cluster:

```console
$ kubectl apply -f gpu_po.yaml
pod/gpu created
```

Check the pod is assigned to gpu node:

```console
$ kubectl get po gpu -owide 
NAME   READY   STATUS      RESTARTS   AGE    IP               NODE    NOMINATED NODE   READINESS GATES
gpu    0/1     Completed   0          104s   192.168.182.14   las3    <none>           <none>
```

See output of the pod:

```console
$ kubectl logs gpu
Thu Aug 28 03:31:47 2025       
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

GPU operator started two process on the GPU hosts using GPU devices:

```console
$ sudo lsof /dev/nvidia-uvm
COMMAND       PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
dcgm-expo 2985974 root   16u   CHR  508,0      0t0  794 /dev/nvidia-uvm
nvidia-de 2986790 root   16u   CHR  508,0      0t0  794 /dev/nvidia-uvm
```

## MIG

Get MIG configs:

```console
$ kubectl -n gpu-operator describe configmap/default-mig-parted-config
Name:         default-mig-parted-config
Namespace:    gpu-operator
Labels:       <none>
Annotations:  <none>

Data
====
config.yaml:
----
version: v1
mig-configs:
  all-disabled:
    - devices: all
      mig-enabled: false

  # A100-40GB, A800-40GB
  all-1g.5gb:
    - devices: all
      mig-enabled: true
      mig-devices:
        "1g.5gb": 7
```

Enable MIG on a node:

```console
$ kubectl label no xxxx nvidia.com/mig.config=all-1g.10gb --overwrite
node/xxxx labeled
```

The default MIG strategy is `single`, which means each MIG instance appears as a `nvidia.com/gpu`. It can be changed to `mixed` during installation by `--set mig.strategy=mixed`.

The `mixed` mode means the MIG instances (appearing as `nvidia.com/mig-1g.10gb`) are coexist with the normal GPUs.

## DRA

Install by `helm`:

```console
$ helm pull nvidia/nvidia-dra-driver-gpu --create-namespace
$ helm install nvidia-dra-driver-gpu nvidia-dra-driver-gpu-25.8.0.tgz --create-namespace --namespace nvidia-dra-driver-gpu --set resources.gpus.enabled=true --set gpuResourcesEnabledOverride=true
NAME: nvidia-dra-driver-gpu
LAST DEPLOYED: Tue Nov 11 18:31:57 2025
NAMESPACE: nvidia-dra-driver-gpu
STATUS: deployed
REVISION: 1
TEST SUITE: None
```

The minimum required Nvidia driver version is: 570.158.01

List installed workloads:

```console
$ kubectl get all -owide -n nvidia-dra-driver-gpu
NAME                                                    READY   STATUS    RESTARTS   AGE   IP                NODE   NOMINATED NODE   READINESS GATES
pod/nvidia-dra-driver-gpu-controller-7b467b555c-7sqgx   1/1     Running   0          55s   192.168.100.146   las0   <none>           <none>
pod/nvidia-dra-driver-gpu-kubelet-plugin-ggclw          2/2     Running   0          55s   192.168.185.46    las3   <none>           <none>

NAME                                                  DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR   AGE   CONTAINERS             IMAGES                                                                                SELECTOR
daemonset.apps/nvidia-dra-driver-gpu-kubelet-plugin   1         1         1       1            1           <none>          55s   compute-domains,gpus   nvcr.io/nvidia/k8s-dra-driver-gpu:v25.8.0,nvcr.io/nvidia/k8s-dra-driver-gpu:v25.8.0   nvidia-dra-driver-gpu-component=kubelet-plugin

NAME                                               READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS       IMAGES                                      SELECTOR
deployment.apps/nvidia-dra-driver-gpu-controller   1/1     1            1           55s   compute-domain   nvcr.io/nvidia/k8s-dra-driver-gpu:v25.8.0   nvidia-dra-driver-gpu-component=controller

NAME                                                          DESIRED   CURRENT   READY   AGE   CONTAINERS       IMAGES                                      SELECTOR
replicaset.apps/nvidia-dra-driver-gpu-controller-7b467b555c   1         1         1       55s   compute-domain   nvcr.io/nvidia/k8s-dra-driver-gpu:v25.8.0   nvidia-dra-driver-gpu-component=controller,pod-template-hash=7b467b555c
```

Note that the kubelet plugin is running on GPU nodes and the controller is running on control plane nodes.

Show installed DeviceClasses:

```console
$ kubectl get deviceclass
NAME                                        AGE
compute-domain-daemon.nvidia.com            2m30s
compute-domain-default-channel.nvidia.com   2m30s
gpu.nvidia.com                              2m30s
mig.nvidia.com                              2m30s
```

List the generated ResouceSlices:

```console
$ kubectl get resourceslice
NAME                                   NODE   DRIVER                      POOL   AGE
las3-compute-domain.nvidia.com-xxckh   las3   compute-domain.nvidia.com   las3   24h
las3-gpu.nvidia.com-m8txf              las3   gpu.nvidia.com              las3   2m59s
```
