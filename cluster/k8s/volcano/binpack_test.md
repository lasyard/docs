# Volcano Binpack 调度实验

使用集群中的两个节点 `las1`, `las2`. 节点的资源是 16 cpu, 8 gpu.

实验设计如下：

在 `las1` 启动一个 Pod, 占用其一半 cpu. Pod 配置如下：

:::{literalinclude} /_files/macos/workspace/k8s/volcano/binpack_cpu_dominant_po.yaml
:::

在 `las2` 启动一个 Pod, 占用其一半 gpu. Pod 配置修改如下：

:::{literalinclude} /_files/macos/workspace/k8s/volcano/binpack_gpu_dominant_po.yaml
:diff: /_files/macos/workspace/k8s/volcano/binpack_cpu_dominant_po.yaml
:::

## 配置 Binpack 以 cpu 为主

修改 Volcano 调度器配置：

```console
$ kubectl edit cm -n volcano-system volcano-scheduler-configmap
```

修改内容如下：

:::{literalinclude} /_files/macos/console/kubectl/get_cm_volcano_scheduler_binpack_cpu.txt
:diff: /_files/macos/console/kubectl/get_cm_volcano_scheduler.txt
:::

这里将 `binpack.weight` 调到很大以减轻其他因素的影响。

启动两个 Pod. 第一个 Pod 使用 1 个 cpu, 配置如下：

:::{literalinclude} /_files/macos/workspace/k8s/volcano/binpack_cpu_only_po.yaml
:::

第二个 Pod 除了使用 1 个 cpu, 还使用一个 gpu, 配置修改如下：

:::{literalinclude} /_files/macos/workspace/k8s/volcano/binpack_cpu_gpu_po.yaml
:diff: /_files/macos/workspace/k8s/volcano/binpack_cpu_only_po.yaml
:::

两个 Pod 启动以后，观察调度结果如下：

```console
$ kubectl get po -owide
NAME           READY   STATUS    RESTARTS   AGE   IP                NODE   NOMINATED NODE   READINESS GATES
cpu-dominant   1/1     Running   0          24s   192.168.221.164   las1   <none>           <none>
cpu-gpu        1/1     Running   0          1s    192.168.221.165   las1   <none>           <none>
cpu-only       1/1     Running   0          5s    192.168.221.151   las1   <none>           <none>
gpu-dominant   1/1     Running   0          20s   192.168.67.165    las2   <none>           <none>
```

可见新启动的 Pod 都被调度到了 cpu 使用率高的节点上。

## 配置 Binpack 以 gpu 为主

修改 Volcano 调度器配置：

```console
$ kubectl edit cm -n volcano-system volcano-scheduler-configmap
```

修改内容如下：

:::{literalinclude} /_files/macos/console/kubectl/get_cm_volcano_scheduler_binpack_gpu.txt
:diff: /_files/macos/console/kubectl/get_cm_volcano_scheduler_binpack_cpu.txt
:::

删除以上两个 Pod:

```console
$ kubectl delete po cpu-only cpu-gpu
pod "cpu-only" deleted
pod "cpu-gpu" deleted
```

重新启动这两个 Pod, 观察调度结果如下：

```console
$ kubectl get po -owide
NAME           READY   STATUS    RESTARTS   AGE   IP                NODE   NOMINATED NODE   READINESS GATES
cpu-dominant   1/1     Running   0          75s   192.168.221.136   las1   <none>           <none>
cpu-gpu        1/1     Running   0          50s   192.168.67.129    las2   <none>           <none>
cpu-only       1/1     Running   0          58s   192.168.221.139   las1   <none>           <none>
gpu-dominant   1/1     Running   0          70s   192.168.67.153    las2   <none>           <none>
```

可见 cpu-only 这个 Pod 仍然被调度到了 cpu 使用率高的节点上，cpu-gpu 这个 Pod 被调度到了 gpu 使用率高的节点上。

## 总结

Volcano 调度器支持 Binpack, 但需要正确配置 binpack 插件参数。

- `binpack.weight` 为打分总权重
- `binpack.cpu` 为 cpu 分数权重
- `binpack.memory` 为 memory 分数权重
- `binpack.resources` 定义了生效的其他/自定义资源，用逗号分隔
- `binpack.resources.nvidia.com/gpu` 为自定义资源 `nvidia.com/gpu` 分数权重
