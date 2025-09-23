# Fake GPU Operator

<https://github.com/run-ai/fake-gpu-operator>

## Install

Pull the helm chart:

```console
$ helm pull oci://ghcr.io/run-ai/fake-gpu-operator/fake-gpu-operator
Pulled: ghcr.io/run-ai/fake-gpu-operator/fake-gpu-operator:0.0.63
Digest: sha256:5538e7eb2391fe77af76b5477d4951a8c7fe9b2a9aaa1b5878c87994bc467b8d
```

Because of the confliction of RuntimeClass `nvidia`, the real GPU Operator must be uninstalled first:

```console
$ helm uninstall gpu-operator -n gpu-operator
release "gpu-operator" uninstalled
```

Create file `fake-gpu-operator-values.yaml` to override the default values:

:::{literalinclude} /_files/macos/workspace/helm/fake-gpu-operator-values.yaml
:::

Here we created two `topology.nodePools` named `h100` and `a100`. There is also a `default` pool in the default values files.

Now label the nodes to use our `pool` settings:

```console
$ kubectl label node las1 run.ai/simulated-gpu-node-pool=default
node/las1 labeled
$ kubectl label node las2 run.ai/simulated-gpu-node-pool=a100
node/las2 labeled
$ kubectl label node las3 run.ai/simulated-gpu-node-pool=h100
node/las3 labeled
```

Then install the Fake GPU Operator:

```console
$ helm upgrade -i gpu-operator fake-gpu-operator-0.0.63.tgz --namespace gpu-operator --create-namespace -f fake-gpu-operator-values.yaml
Release "gpu-operator" does not exist. Installing it now.
NAME: gpu-operator
LAST DEPLOYED: Tue Sep 23 13:56:11 2025
NAMESPACE: gpu-operator
STATUS: deployed
REVISION: 1
TEST SUITE: None
```

List the running pods:

```console
$ kubectl get po -n gpu-operator -owide
NAME                                      READY   STATUS    RESTARTS   AGE     IP                NODE   NOMINATED NODE   READINESS GATES
device-plugin-6rpxv                       1/1     Running   0          2m31s   192.168.185.53    las3   <none>           <none>
device-plugin-7ltdt                       1/1     Running   0          2m31s   192.168.67.160    las2   <none>           <none>
device-plugin-brrmf                       1/1     Running   0          2m31s   192.168.221.163   las1   <none>           <none>
kwok-gpu-device-plugin-5c68bdbb58-jbdsd   1/1     Running   0          7m55s   192.168.67.153    las2   <none>           <none>
nvidia-dcgm-exporter-fxsn2                1/1     Running   0          2m7s    192.168.185.9     las3   <none>           <none>
nvidia-dcgm-exporter-wbrqz                1/1     Running   0          2m7s    192.168.67.166    las2   <none>           <none>
nvidia-dcgm-exporter-x4s6g                1/1     Running   0          2m8s    192.168.221.164   las1   <none>           <none>
status-updater-5bdc9dd8cb-6mt4v           1/1     Running   0          7m55s   192.168.185.48    las3   <none>           <none>
topology-server-67947cbd54-kgj99          1/1     Running   0          7m55s   192.168.185.28    las3   <none>           <none>
```

The is one `device-plugin` for each labelled node.

List the GPU devices:

```console
$ kubectl get no -o custom-columns=NAME:.metadata.name,GPU:.status.capacity.nvidia\\.com/gpu
NAME   GPU
las0   <none>
las1   2
las2   8
las3   8
```

## Usage

Apply the following file to create GPU pod:

:::{literalinclude} /_files/macos/workspace/k8s/fake_gpu_po.yaml
:::

The env `NODE_NAME` is crucial to make the fake `nvidia-smi` work. After the pod is running, execute `nvidia-smi` in the pod:

```console
$ kubectl exec gpu -- nvidia-smi
Tue Sep 23 09:36:52 2025
+------------------------------------------------------------------------------+
| NVIDIA-SMI 470.129.06   Driver Version: 470.129.06   CUDA Version: 11.4      |
+--------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M | Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap |         Memory-Usage | GPU-Util  Compute M. |
|                                |                      |               MIG M. |
+--------------------------------+----------------------+----------------------+
|   0  H100                  Off | 00000001:00:00.0 Off |                  Off |
| N/A   33C    P8    11W /  70W  |  83968MiB / 83968MiB |     100%     Default |
|                                |                      |                  N/A |
+--------------------------------+----------------------+----------------------+

+------------------------------------------------------------------------------+
| Processes:                                                                   |
|  GPU   GI   CI        PID   Type   Process name                  GPU Memory  |
|        ID   ID                                                   Usage       |
+------------------------------------------------------------------------------+
|    0   N/A  N/A       8        G   sh-ctrap exit INT TERM; s..    83968MiB   |
+------------------------------------------------------------------------------+
```

Not all the cards are shown. Actually, there is no `/dev/nvidia*` device files at all.

## Pitfalls

The active conf for fake GPUs is stored in ConfigMaps:

```console
$ kubectl get cm -n gpu-operator
NAME               DATA   AGE
hostpath-init      1      10m
kube-root-ca.crt   1      10m
topology           1      10m
topology-las1      1      10m
topology-las2      1      10m
topology-las3      1      10m
```

Unfortunately, if you re-label a node to change its fake GPU pool, the modification will not take effect automatically, even after the operator is reinstalled. The ConfigMap `topology-<NODE_NAME>`s are not deleted when the operator is uninstalled.

To make it effective, you need to delete the corresponding `topology-<NODE_NAME>`, then restart `status-updater`:

```console
$ kubectl rollout restart deploy status-updater -n gpu-operator
deployment.apps/status-updater restarted
```

This will regenerate `topology-<NODE_NAME>`. To make it effective on the node, the device plugin on the node must be restarted.
