# 配置 kubelet 节点 NUMA-Aware

## 节点信息

在节点上查看 NUMA 拓扑：

```console
$ numactl -H
available: 2 nodes (0-1)
node 0 cpus: 0 2 4 6 8 10 12 14 16 18 20 22 24 26 28 30 32 34 36 38 40 42 44 46 48 50 52 54 56 58 60 62
node 0 size: 128320 MB
node 0 free: 15904 MB
node 1 cpus: 1 3 5 7 9 11 13 15 17 19 21 23 25 27 29 31 33 35 37 39 41 43 45 47 49 51 53 55 57 59 61 63
node 1 size: 128964 MB
node 1 free: 20287 MB
node distances:
node   0   1 
  0:  10  21 
  1:  21  10
```

可见主机上有两个 NUMA 节点。

配置前查看 kubelet CPU 管理状态：

```console
$ sudo cat /var/lib/kubelet/cpu_manager_state | jq
{
  "policyName": "none",
  "defaultCpuSet": "",
  "checksum": 1353318690
}
```

## 配置

开始配置。修改 kubelet 配置文件（一般是 `/var/lib/kubelet/config.yaml`，可以通过 `systemctl cat kubelet` 查看）：

```yaml
featureGates:
  CPUManagerPolicyOptions: true
  CPUManagerPolicyAlphaOptions: true
enforceNodeAllocatable:
  - pods
cpuManagerPolicy: static
cpuManagerPolicyOptions:
  strict-cpu-reservation: "true"
  align-by-socket: "true"
reservedSystemCPUs: "0-3"
memoryManagerPolicy: Static
evictionHard:
  memory.available: 2Gi
evictionSoft:
  memory.available: 4Gi
kubeReserved:
  memory: 1Gi
systemReserved:
  memory: 1Gi
reservedMemory:
  - numaNode: 0
    limits:
      memory: 2Gi
  - numaNode: 1
    limits:
      memory: 2Gi
topologyManagerPolicy: best-effort
topologyManagerScope: pod
```

:::{note}
配置中需要注意以下几点：

- 内存数量：`reservedMemory` 中所有 NUMA 节点的和 = `kubeReserved` + `systemReserved` + `evictionHard`
- `cpuManagerPolicy` 为 `static`, 而 `memoryManagerPolicy` 为 `Static`, 大小写敏感
- `reservedSystemCPUs` 为系统预留 CPU, 目的是将其他 CPU 空出来给其他 Workload 用，实际需要采用其他手段控制系统的 CPU 使用，见附录
- `reservedSystemCPUs` 与 `systemReservedCgroup` 和 `kubeReservedCgroup` 选项不可同时配置，否则会得到以下错误：

   ```text
   invalid configuration: can't use reservedSystemCPUs (--reserved-cpus) with systemReservedCgroup (--system-reserved-cgroup) or kubeReservedCgroup (--kube-reserved-cgroup)
   ```

:::

配置完成后重启 kubelet:

```console
$ sudo systemctl restart kubelet
```

重启成功后查看 kubelet CPU 管理状态：

```console
$ sudo cat /var/lib/kubelet/cpu_manager_state | jq
{
  "policyName": "static",
  "defaultCpuSet": "5,7,9,11,13,15,17,19-31,33,35,37,39,41,43,45,47,49,51-63",
  "entries": {
    "5317fc13-8a4d-4ebf-ba4c-382fe072e5a2": {
      "nerdctl-api": "4,6,8,10,12,14,16,18,36,38,40,42,44,46,48,50"
    },
    "c5284f88-2b28-43b1-9cf1-a35d28e854ea": {
      "quota-plugin": "32"
    },
    "f0ad8a75-b43c-4e26-b8ec-a7fabf1488c6": {
      "validator-plugin": "34"
    }
  },
  "checksum": 577098591
}
```

出现在 `entries` 中的条目是被各个容器占据的 CPU, 这些 CPU 被排除在 `defaultCpuSet`, 不能再调度其他容器。可以看到基本上每个容器的 CPU 都在同一个 NUMA 节点内。

## 实验

编辑一个 Pod 配置文件 `numa_po.yaml`:

:::{literalinclude} /_files/macos/workspace/k8s/numa_po.yaml
:::

在集群中创建：

```console
$ kubectl create -f numa_po.yaml 
pod/numa-czxg2 created
$ kubectl get po -l for=test
NAME         READY   STATUS    RESTARTS   AGE
numa-czxg2   1/1     Running   0          6s
```

再次查看 kubelet CPU 管理状态：

```console
$ sudo cat /var/lib/kubelet/cpu_manager_state | jq
{
  "policyName": "static",
  "defaultCpuSet": "5,7,9,11,13,15,17,19,21,23,25,27-31,33,35,37,39,41,43,45,47,49,51,53,55,57,59-63",
  "entries": {
    "2af4b2d2-cc9b-4ae5-9f53-271e1a61f9d6": {
      "numa": "20,22,24,26,52,54,56,58"
    },
    "5317fc13-8a4d-4ebf-ba4c-382fe072e5a2": {
      "nerdctl-api": "4,6,8,10,12,14,16,18,36,38,40,42,44,46,48,50"
    },
    "c5284f88-2b28-43b1-9cf1-a35d28e854ea": {
      "quota-plugin": "32"
    },
    "f0ad8a75-b43c-4e26-b8ec-a7fabf1488c6": {
      "validator-plugin": "34"
    }
  },
  "checksum": 191855977
}
```

可见名为 `numa` 的容器分配到了应有的 CPU 数量并在同一个 NUMA 节点内。另外，通过文件 `/var/lib/kubelet/memory_manager_state` 可以看到内存管理状态。

修改 Pod 配置文件：

:::{literalinclude} /_files/macos/workspace/k8s/numa_po_1.yaml
:diff: /_files/macos/workspace/k8s/numa_po.yaml
:::

运行后再次查看 kubelet CPU 管理状态可以发现状态没有变化。事实上，kubelet 只对 Qos Class 为 Guaranteed 的 Pod 进行 NUMA 亲和性的分配，请参阅 [Configure Quality of Service for Pods](https://kubernetes.io/docs/tasks/configure-pod-container/quality-service-pod/). 具体来说：

1. 当 Pod 的所有容器都设置了 `cpu` 和 `memory` 资源的 `requests` 和 `limits` 值，并且 `requests.cpu == limits.cpu && requests.memory == limits.memory` 时，Qos Class 为 Guaranteed
2. 当 Pod 的所有容器都没有设置任何 `cpu` 和 `memory` 的 `requests` 和 `limits` 值时，Qos Class 为 BestEffort
3. 以上两种情形之外，Qos Class 为 Burstable

对于不参与 NUMA 亲和性分配的 Pod 来说，申请的 cpu 不占用专有 CPU, 申请的 memory 虽然不体现在 `memory_manager_state` 文件中，但将导致总内存减少。
