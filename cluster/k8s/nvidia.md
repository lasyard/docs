# NVIDIA GPU Operator

Add repository:

```console
$ helm repo add nvidia https://helm.ngc.nvidia.com/nvidia
"nvidia" has been added to your repositories
```

Install:

```console
$ helm pull nvidia/gpu-operator --version=v25.3.0
$ helm install gpu-operator -n gpu-operator --create-namespace gpu-operator-v25.3.0.tgz --set driver.enabled=false
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
:language: yaml
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
Tue Apr 22 10:27:26 2025       
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 560.35.05              Driver Version: 560.35.05      CUDA Version: 12.6     |
|-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  NVIDIA L40S                    Off |   00000000:00:05.0 Off |                    0 |
| N/A   26C    P8             23W /  350W |       1MiB /  46068MiB |      0%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+
                                                                                         
+-----------------------------------------------------------------------------------------+
| Processes:                                                                              |
|  GPU   GI   CI        PID   Type   Process name                              GPU Memory |
|        ID   ID                                                               Usage      |
|=========================================================================================|
|  No running processes found                                                             |
+-----------------------------------------------------------------------------------------+
```
