# Kubeflow PyTorchJob 调度实验

## 实验内容

PyTorchJob 定义：

:::{literalinclude} /_files/macos/workspace/k8s/kubeflow/pytorchjob.yaml
:::

### 正常情况

提交以上 PyTorchjob:

```console
$ kubectl apply -f pytorchjob.yaml
pytorchjob.kubeflow.org/pytest created
```

监视 PyTorchJob 状态变化：

```console
$ kubectl get pytorchjob -owide -w
NAME     STATE   AGE
pytest           0s
pytest   Created   0s
pytest   Created   1s
pytest   Running   3s
pytest   Running   7s
pytest   Running   7s
pytest   Running   8s
pytest   Succeeded   35s
pytest   Succeeded   35s
```

监视 PodGroup 状态变化：

```console
$ kubectl get podgroup -owide -w
NAME     STATUS   MINMEMBER   RUNNINGS   AGE   QUEUE
pytest            4                      0s    default
pytest   Inqueue   4                      1s    default
pytest   Running   4                      2s    default
pytest   Running   4           1          4s    default
pytest   Running   4           3          7s    default
pytest   Running   4           4          8s    default
pytest   Running   4           4          35s   default
```

监视 Pod 状态变化：

```console
$ kubectl get po -owide -w
NAME              READY   STATUS    RESTARTS   AGE   IP       NODE     NOMINATED NODE   READINESS GATES
pytest-master-0   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
pytest-worker-0   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
pytest-worker-1   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
pytest-worker-2   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
pytest-master-0   0/1     Pending   0          1s    <none>   las1     <none>           <none>
pytest-worker-1   0/1     Pending   0          1s    <none>   las1     <none>           <none>
pytest-worker-0   0/1     Pending   0          1s    <none>   las1     <none>           <none>
pytest-worker-2   0/1     Pending   0          1s    <none>   las1     <none>           <none>
pytest-master-0   0/1     ContainerCreating   0          1s    <none>   las1     <none>           <none>
pytest-worker-1   0/1     Init:0/1            0          1s    <none>   las1     <none>           <none>
pytest-worker-2   0/1     Init:0/1            0          1s    <none>   las1     <none>           <none>
pytest-worker-0   0/1     Init:0/1            0          1s    <none>   las1     <none>           <none>
pytest-master-0   0/1     ContainerCreating   0          1s    <none>   las1     <none>           <none>
pytest-worker-1   0/1     Init:0/1            0          2s    <none>   las1     <none>           <none>
pytest-worker-0   0/1     Init:0/1            0          2s    <none>   las1     <none>           <none>
pytest-worker-2   0/1     Init:0/1            0          2s    <none>   las1     <none>           <none>
pytest-worker-2   0/1     Init:0/1            0          2s    192.168.221.159   las1     <none>           <none>
pytest-master-0   1/1     Running             0          2s    192.168.221.161   las1     <none>           <none>
pytest-worker-0   0/1     Init:0/1            0          2s    192.168.221.184   las1     <none>           <none>
pytest-worker-1   0/1     Init:0/1            0          3s    192.168.221.183   las1     <none>           <none>
pytest-worker-0   0/1     PodInitializing     0          4s    192.168.221.184   las1     <none>           <none>
pytest-worker-1   0/1     PodInitializing     0          4s    192.168.221.183   las1     <none>           <none>
pytest-worker-2   0/1     PodInitializing     0          5s    192.168.221.159   las1     <none>           <none>
pytest-worker-1   1/1     Running             0          5s    192.168.221.183   las1     <none>           <none>
pytest-worker-0   1/1     Running             0          6s    192.168.221.184   las1     <none>           <none>
pytest-worker-2   1/1     Running             0          6s    192.168.221.159   las1     <none>           <none>
pytest-master-0   0/1     Completed           0          33s   192.168.221.161   las1     <none>           <none>
pytest-master-0   0/1     Completed           0          34s   192.168.221.161   las1     <none>           <none>
pytest-master-0   0/1     Completed           0          34s   192.168.221.161   las1     <none>           <none>
pytest-worker-1   0/1     Completed           0          36s   192.168.221.183   las1     <none>           <none>
pytest-worker-0   0/1     Completed           0          36s   192.168.221.184   las1     <none>           <none>
pytest-worker-2   0/1     Completed           0          37s   192.168.221.159   las1     <none>           <none>
pytest-worker-1   0/1     Completed           0          37s   192.168.221.183   las1     <none>           <none>
pytest-worker-0   0/1     Completed           0          37s   192.168.221.184   las1     <none>           <none>
pytest-worker-1   0/1     Completed           0          37s   192.168.221.183   las1     <none>           <none>
pytest-worker-0   0/1     Completed           0          37s   192.168.221.184   las1     <none>           <none>
pytest-worker-2   0/1     Completed           0          38s   192.168.221.159   las1     <none>           <none>
pytest-worker-2   0/1     Completed           0          38s   192.168.221.159   las1     <none>           <none>
```

可以观察到作业启动时创建了一个与 PyTorchJob 同名的 PodGroup 且 `minMember` 被设置为 Master 与 Worker 的副本数之和。另外，由于 binpack 策略的存在，所有 Pod 被放在了同一个节点上。进一步观察可知 PyTorchJob 成功后，PodGroup 被删除，Pod 仍存在。

另外可以观察到，PyTorchJob 的状态变为 Running 是在 Master Pod 变为 Running 之后，而此时还有 Worker 没有进入 Running 状态；同样的，状态变为 Succeeded 是在 Master Pod 变为 Completed 之后，此时还有 Worker 没有运行结束。初步得出结论，PyTorchJob 的状态变化主要由 Master Pod 的状态决定。

为了验证是否存在 gang 策略，修改队列 default 的容量：

```console
$ kubectl edit q default
```

修改内容如下：

:::{literalinclude} /_files/macos/console/kubectl/get_q_default_2c.txt
:diff: /_files/macos/console/kubectl/get_q_default.txt
:::

重新提交作业并监视状态：

```console
kubectl get pytorchjob -owide -w
NAME     STATE   AGE
pytest           0s
pytest   Created   0s
pytest   Created   1s
```

```console
kubectl get podgroup -owide -w
NAME     STATUS   MINMEMBER   RUNNINGS   AGE   QUEUE
pytest            4                      0s    default
pytest   Inqueue   4                      1s    default
pytest   Inqueue   4                      2s    default
```

```console
kubectl get po -owide -w
NAME              READY   STATUS    RESTARTS   AGE   IP       NODE     NOMINATED NODE   READINESS GATES
pytest-master-0   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
pytest-worker-0   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
pytest-worker-1   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
pytest-worker-2   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
pytest-worker-2   0/1     Pending   0          1s    <none>   <none>   <none>           <none>
pytest-master-0   0/1     Pending   0          1s    <none>   <none>   <none>           <none>
pytest-worker-1   0/1     Pending   0          1s    <none>   <none>   <none>           <none>
pytest-worker-0   0/1     Pending   0          1s    <none>   <none>   <none>           <none>
```

可见当队列容量小于作业所需的总容量时，作业无法运行，PodGroup 处于 Inqueue 状态。

Master 环境变量：

```console
$ kubectl describe pod pytest-master-0
...
    Environment:
      PYTHONUNBUFFERED:    1
      MASTER_PORT:         23456
      PET_MASTER_PORT:     23456
      MASTER_ADDR:         pytest-master-0
      PET_MASTER_ADDR:     pytest-master-0
      WORLD_SIZE:          4
      RANK:                0
      PET_NODE_RANK:       0
      PET_NPROC_PER_NODE:  auto
      PET_NNODES:          4
...
```

Worker 环境变量：

```console
$ kubectl describe pod pytest-worker-0
...
    Environment:
      PYTHONUNBUFFERED:    1
      MASTER_PORT:         23456
      PET_MASTER_PORT:     23456
      MASTER_ADDR:         pytest-master-0
      PET_MASTER_ADDR:     pytest-master-0
      WORLD_SIZE:          4
      RANK:                1
      PET_NODE_RANK:       1
      PET_NPROC_PER_NODE:  auto
      PET_NNODES:          4
...
```

`RANK` 的值各不相同，从 `0` 到 `WORLD_SIZE - 1`, 而 Master 的 `RANK` 为 `0`.

如果修改 `spec.pytorchReplicaSpecs.Master.replicas` 为 2 再提交，将收到错误信息：

```console
$ kubectl apply -f pytorchjob.yaml
Error from server (Forbidden): error when creating "pytorchjob.yaml": admission webhook "validator.pytorchjob.training-operator.kubeflow.org" denied the request: spec.pytorchReplicaSpecs[Master].replicas: Forbidden: must be 1
```

根据以上实验（以及一些微调参数以后的实验）结果可得出以下结论：

- Master 的副本数只能是 1
- PyTorchJob 的状态基本只跟 Master Pod 的状态相关
- PodGroup 的 MinMember 被设为 Master 与 Worker 的副本数之和
- PyTorchJob 成功后 PodGroup 被删除，Pod 仍保留
- Volcano 的 binpack 和 gang 策略有效

### 部分 Worker 失败情形

修改 PyTorchJob 定义：

:::{literalinclude} /_files/macos/workspace/k8s/kubeflow/pytorchjob_fail_1_worker.yaml
:diff: /_files/macos/workspace/k8s/kubeflow/pytorchjob.yaml
:::

通过修改启动脚本人为使一个 Worker 失败，然后提交。

监视 PyTorchJob 状态变化：

```console
$ kubectl get pytorchjob -owide -w
NAME     STATE   AGE
pytest           0s
pytest   Created   0s
pytest   Created   1s
pytest   Running   4s
pytest   Running   7s
pytest   Running   7s
pytest   Succeeded   35s
pytest   Succeeded   35s
```

监视 PodGroup 状态变化：

```console
$ kubectl get podgroup -owide -w
NAME     STATUS   MINMEMBER   RUNNINGS   AGE   QUEUE
pytest            4                      0s    default
pytest   Inqueue   4                      1s    default
pytest   Running   4                      2s    default
pytest   Running   4           1          4s    default
pytest   Running   4           4          7s    default
pytest   Running   4           4          35s   default
```

监视 Pod 状态变化：

```console
$ kubectl get po -owide -w
NAME              READY   STATUS    RESTARTS   AGE   IP       NODE     NOMINATED NODE   READINESS GATES
pytest-master-0   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
pytest-worker-0   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
pytest-worker-1   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
pytest-worker-2   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
pytest-worker-2   0/1     Pending   0          1s    <none>   las1     <none>           <none>
pytest-worker-0   0/1     Pending   0          1s    <none>   las1     <none>           <none>
pytest-worker-1   0/1     Pending   0          1s    <none>   las1     <none>           <none>
pytest-master-0   0/1     Pending   0          1s    <none>   las1     <none>           <none>
pytest-worker-2   0/1     Init:0/1   0          1s    <none>   las1     <none>           <none>
pytest-worker-1   0/1     Init:0/1   0          1s    <none>   las1     <none>           <none>
pytest-master-0   0/1     ContainerCreating   0          1s    <none>   las1     <none>           <none>
pytest-worker-0   0/1     Init:0/1            0          1s    <none>   las1     <none>           <none>
pytest-worker-2   0/1     Init:0/1            0          2s    <none>   las1     <none>           <none>
pytest-worker-1   0/1     Init:0/1            0          2s    <none>   las1     <none>           <none>
pytest-master-0   0/1     ContainerCreating   0          2s    <none>   las1     <none>           <none>
pytest-worker-0   0/1     Init:0/1            0          2s    <none>   las1     <none>           <none>
pytest-worker-1   0/1     Init:0/1            0          3s    192.168.221.157   las1     <none>           <none>
pytest-master-0   1/1     Running             0          3s    192.168.221.130   las1     <none>           <none>
pytest-worker-2   0/1     Init:0/1            0          3s    192.168.221.182   las1     <none>           <none>
pytest-worker-0   0/1     Init:0/1            0          3s    192.168.221.149   las1     <none>           <none>
pytest-worker-2   0/1     PodInitializing     0          5s    192.168.221.182   las1     <none>           <none>
pytest-worker-0   0/1     PodInitializing     0          5s    192.168.221.149   las1     <none>           <none>
pytest-worker-1   0/1     PodInitializing     0          5s    192.168.221.157   las1     <none>           <none>
pytest-worker-1   1/1     Running             0          6s    192.168.221.157   las1     <none>           <none>
pytest-worker-2   1/1     Running             0          6s    192.168.221.182   las1     <none>           <none>
pytest-worker-0   1/1     Running             0          6s    192.168.221.149   las1     <none>           <none>
pytest-worker-0   0/1     Error               0          16s   192.168.221.149   las1     <none>           <none>
pytest-worker-0   1/1     Running             1 (2s ago)   17s   192.168.221.149   las1     <none>           <none>
pytest-worker-0   0/1     Error               1 (12s ago)   27s   192.168.221.149   las1     <none>           <none>
pytest-master-0   0/1     Completed           0             33s   192.168.221.130   las1     <none>           <none>
pytest-master-0   0/1     Completed           0             34s   192.168.221.130   las1     <none>           <none>
pytest-master-0   0/1     Completed           0             34s   192.168.221.130   las1     <none>           <none>
pytest-worker-1   0/1     Completed           0             36s   192.168.221.157   las1     <none>           <none>
pytest-worker-2   0/1     Completed           0             36s   192.168.221.182   las1     <none>           <none>
pytest-worker-1   0/1     Completed           0             37s   192.168.221.157   las1     <none>           <none>
pytest-worker-2   0/1     Completed           0             37s   192.168.221.182   las1     <none>           <none>
pytest-worker-1   0/1     Completed           0             37s   192.168.221.157   las1     <none>           <none>
pytest-worker-2   0/1     Completed           0             37s   192.168.221.182   las1     <none>           <none>
pytest-worker-0   0/1     CrashLoopBackOff    1 (12s ago)   38s   192.168.221.149   las1     <none>           <none>
pytest-worker-0   1/1     Running             2 (13s ago)   39s   192.168.221.149   las1     <none>           <none>
pytest-worker-0   0/1     Error               2 (23s ago)   49s   192.168.221.149   las1     <none>           <none>
pytest-worker-0   0/1     CrashLoopBackOff    2 (12s ago)   60s   192.168.221.149   las1     <none>           <none>
pytest-worker-0   1/1     Running             3 (27s ago)   75s   192.168.221.149   las1     <none>           <none>
pytest-worker-0   0/1     Error               3 (37s ago)   85s   192.168.221.149   las1     <none>           <none>
pytest-worker-0   0/1     CrashLoopBackOff    3 (15s ago)   99s   192.168.221.149   las1     <none>           <none>
pytest-worker-0   1/1     Running             4 (43s ago)   2m7s   192.168.221.149   las1     <none>           <none>
pytest-worker-0   0/1     Error               4 (53s ago)   2m17s   192.168.221.149   las1     <none>           <none>
pytest-worker-0   0/1     CrashLoopBackOff    4 (12s ago)   2m28s   192.168.221.149   las1     <none>           <none>
pytest-worker-0   1/1     Running             5 (83s ago)   3m39s   192.168.221.149   las1     <none>           <none>
pytest-worker-0   0/1     Error               5 (93s ago)   3m49s   192.168.221.149   las1     <none>           <none>
pytest-worker-0   0/1     CrashLoopBackOff    5 (16s ago)   4m3s    192.168.221.149   las1     <none>           <none>
```

可见某个 Worker 失败对 PyTorchJob 没有影响，并且由于设置了 `restartPolicy` 为 `OnFailure`, 失败的 Worker 一直在重启，且重启次数不受 `spec.runPolicy.backoffLimit` 设置的影响。

### 全部 Worker 失败情形

修改 PyTorchJob 定义：

:::{literalinclude} /_files/macos/workspace/k8s/kubeflow/pytorchjob_fail_all_workers.yaml
:diff: /_files/macos/workspace/k8s/kubeflow/pytorchjob.yaml
:::

提交以后，监视 PyTorchJob 状态变化：

```console
$ kubectl get pytorchjob -owide -w
NAME     STATE   AGE
pytest           0s
pytest   Created   0s
pytest   Created   1s
pytest   Running   3s
pytest   Running   7s
pytest   Running   7s
pytest   Failed    18s
```

监视 PodGroup 状态变化：

```console
$ kubectl get podgroup -owide -w
NAME     STATUS   MINMEMBER   RUNNINGS   AGE   QUEUE
pytest            4                      0s    default
pytest   Inqueue   4                      1s    default
pytest   Running   4                      2s    default
pytest   Running   4           1          4s    default
pytest   Running   4           4          8s    default
pytest   Running   4           4          18s   default
```

监视 Pod 状态变化：

```console
$ kubectl get po -owide -w
NAME              READY   STATUS    RESTARTS   AGE   IP       NODE     NOMINATED NODE   READINESS GATES
pytest-worker-0   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
pytest-worker-1   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
pytest-worker-2   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
pytest-master-0   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
pytest-master-0   0/1     Pending   0          1s    <none>   las1     <none>           <none>
pytest-worker-0   0/1     Pending   0          1s    <none>   las1     <none>           <none>
pytest-worker-1   0/1     Pending   0          1s    <none>   las1     <none>           <none>
pytest-worker-2   0/1     Pending   0          1s    <none>   las1     <none>           <none>
pytest-master-0   0/1     ContainerCreating   0          1s    <none>   las1     <none>           <none>
pytest-worker-0   0/1     Init:0/1            0          1s    <none>   las1     <none>           <none>
pytest-worker-1   0/1     Init:0/1            0          1s    <none>   las1     <none>           <none>
pytest-worker-2   0/1     Init:0/1            0          1s    <none>   las1     <none>           <none>
pytest-master-0   0/1     ContainerCreating   0          1s    <none>   las1     <none>           <none>
pytest-worker-0   0/1     Init:0/1            0          1s    <none>   las1     <none>           <none>
pytest-worker-2   0/1     Init:0/1            0          2s    <none>   las1     <none>           <none>
pytest-worker-1   0/1     Init:0/1            0          2s    <none>   las1     <none>           <none>
pytest-worker-1   0/1     Init:0/1            0          2s    192.168.221.166   las1     <none>           <none>
pytest-worker-0   0/1     Init:0/1            0          2s    192.168.221.142   las1     <none>           <none>
pytest-worker-2   0/1     Init:0/1            0          2s    192.168.221.178   las1     <none>           <none>
pytest-master-0   1/1     Running             0          2s    192.168.221.172   las1     <none>           <none>
pytest-worker-0   0/1     PodInitializing     0          5s    192.168.221.142   las1     <none>           <none>
pytest-worker-1   0/1     PodInitializing     0          5s    192.168.221.166   las1     <none>           <none>
pytest-worker-2   0/1     PodInitializing     0          5s    192.168.221.178   las1     <none>           <none>
pytest-worker-2   1/1     Running             0          6s    192.168.221.178   las1     <none>           <none>
pytest-worker-0   1/1     Running             0          6s    192.168.221.142   las1     <none>           <none>
pytest-worker-1   1/1     Running             0          6s    192.168.221.166   las1     <none>           <none>
pytest-worker-2   0/1     Error               0          16s   192.168.221.178   las1     <none>           <none>
pytest-worker-0   0/1     Error               0          16s   192.168.221.142   las1     <none>           <none>
pytest-worker-1   0/1     Error               0          16s   192.168.221.166   las1     <none>           <none>
pytest-worker-1   1/1     Running             1 (2s ago)   17s   192.168.221.166   las1     <none>           <none>
pytest-worker-0   1/1     Running             1 (2s ago)   17s   192.168.221.142   las1     <none>           <none>
pytest-worker-2   1/1     Running             1 (2s ago)   17s   192.168.221.178   las1     <none>           <none>
pytest-worker-2   1/1     Terminating         1 (2s ago)   17s   192.168.221.178   las1     <none>           <none>
pytest-master-0   1/1     Terminating         0            17s   192.168.221.172   las1     <none>           <none>
pytest-worker-0   1/1     Terminating         1 (2s ago)   17s   192.168.221.142   las1     <none>           <none>
pytest-worker-1   1/1     Terminating         1 (2s ago)   17s   192.168.221.166   las1     <none>           <none>
pytest-master-0   1/1     Terminating         0            18s   192.168.221.172   las1     <none>           <none>
pytest-master-0   0/1     Error               0            18s   192.168.221.172   las1     <none>           <none>
pytest-master-0   0/1     Error               0            18s   192.168.221.172   las1     <none>           <none>
pytest-master-0   0/1     Error               0            18s   192.168.221.172   las1     <none>           <none>
pytest-worker-1   1/1     Terminating         1 (3s ago)   18s   192.168.221.166   las1     <none>           <none>
pytest-worker-0   1/1     Terminating         1 (3s ago)   18s   192.168.221.142   las1     <none>           <none>
pytest-worker-2   1/1     Terminating         1 (4s ago)   19s   192.168.221.178   las1     <none>           <none>
pytest-worker-1   0/1     Error               1 (4s ago)   19s   192.168.221.166   las1     <none>           <none>
pytest-worker-0   0/1     Error               1 (4s ago)   19s   192.168.221.142   las1     <none>           <none>
pytest-worker-2   0/1     Error               1 (4s ago)   19s   192.168.221.178   las1     <none>           <none>
pytest-worker-0   0/1     Error               1 (4s ago)   19s   192.168.221.142   las1     <none>           <none>
pytest-worker-0   0/1     Error               1 (4s ago)   19s   192.168.221.142   las1     <none>           <none>
pytest-worker-1   0/1     Error               1 (4s ago)   19s   192.168.221.166   las1     <none>           <none>
pytest-worker-1   0/1     Error               1 (4s ago)   19s   192.168.221.166   las1     <none>           <none>
pytest-worker-2   0/1     Error               1 (4s ago)   19s   192.168.221.178   las1     <none>           <none>
pytest-worker-2   0/1     Error               1 (4s ago)   19s   192.168.221.178   las1     <none>           <none>
```

可以看到 Kubeflow 检测到了所有 Worker 失败并将 PyTorchJob 状态置为 Failed, 不执行重启。进一步检查发现此时所有 Pod 和 PodGroup 已被删除。另外可发现 Pod 被删除前试图重启。

进一步实验可表明，如果在 Master 存续期间没有发生全体 Worker 失败（至少有一个 Worker 已完成或还在运行），则 Master 完成后 PyTorchJob 状态仍然是 Succeeded.

### Master 失败情形

修改 PyTorchJob 定义：

:::{literalinclude} /_files/macos/workspace/k8s/kubeflow/pytorchjob_fail_master.yaml
:diff: /_files/macos/workspace/k8s/kubeflow/pytorchjob.yaml
:::

提交以后，监视 PyTorchJob 状态变化：

```console
$ kubectl get pytorchjob -owide -w
NAME     STATE   AGE
pytest           0s
pytest   Created   0s
pytest   Created   1s
pytest   Running   3s
pytest   Running   5s
pytest   Running   7s
pytest   Running   8s
pytest   Running   37s
pytest   Running   39s
pytest   Running   39s
pytest   Failed    2m16s
```

监视 PodGroup 状态变化：

```console
$ kubectl get podgroup -owide -w
NAME     STATUS   MINMEMBER   RUNNINGS   AGE   QUEUE
pytest            4                      0s    default
pytest   Inqueue   4                      1s    default
pytest   Running   4                      2s    default
pytest   Running   4           1          4s    default
pytest   Running   4           2          6s    default
pytest   Running   4           4          8s    default
pytest   Running   4           3          37s   default
pytest   Running   4           1          39s   default
pytest   Running   4           1          2m16s   default
```

监视 Pod 状态变化：

```console
$ kubectl get po -owide -w
NAME              READY   STATUS    RESTARTS   AGE   IP       NODE     NOMINATED NODE   READINESS GATES
pytest-master-0   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
pytest-worker-0   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
pytest-worker-1   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
pytest-worker-2   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
pytest-master-0   0/1     Pending   0          1s    <none>   las1     <none>           <none>
pytest-worker-2   0/1     Pending   0          1s    <none>   las1     <none>           <none>
pytest-worker-1   0/1     Pending   0          1s    <none>   las1     <none>           <none>
pytest-worker-0   0/1     Pending   0          1s    <none>   las1     <none>           <none>
pytest-master-0   0/1     ContainerCreating   0          1s    <none>   las1     <none>           <none>
pytest-worker-2   0/1     Init:0/1            0          1s    <none>   las1     <none>           <none>
pytest-worker-1   0/1     Init:0/1            0          1s    <none>   las1     <none>           <none>
pytest-worker-0   0/1     Init:0/1            0          1s    <none>   las1     <none>           <none>
pytest-master-0   0/1     ContainerCreating   0          2s    <none>   las1     <none>           <none>
pytest-worker-2   0/1     Init:0/1            0          2s    <none>   las1     <none>           <none>
pytest-worker-1   0/1     Init:0/1            0          2s    <none>   las1     <none>           <none>
pytest-worker-0   0/1     Init:0/1            0          2s    <none>   las1     <none>           <none>
pytest-worker-1   0/1     Init:0/1            0          2s    192.168.221.152   las1     <none>           <none>
pytest-master-0   1/1     Running             0          2s    192.168.221.140   las1     <none>           <none>
pytest-worker-2   0/1     Init:0/1            0          2s    192.168.221.162   las1     <none>           <none>
pytest-worker-0   0/1     PodInitializing     0          3s    192.168.221.177   las1     <none>           <none>
pytest-worker-0   1/1     Running             0          4s    192.168.221.177   las1     <none>           <none>
pytest-worker-1   0/1     PodInitializing     0          5s    192.168.221.152   las1     <none>           <none>
pytest-worker-2   0/1     PodInitializing     0          5s    192.168.221.162   las1     <none>           <none>
pytest-worker-1   1/1     Running             0          6s    192.168.221.152   las1     <none>           <none>
pytest-worker-2   1/1     Running             0          6s    192.168.221.162   las1     <none>           <none>
pytest-master-0   0/1     Error               0          33s   192.168.221.140   las1     <none>           <none>
pytest-master-0   1/1     Running             1 (2s ago)   34s   192.168.221.140   las1     <none>           <none>
pytest-worker-0   0/1     Completed           0            35s   192.168.221.177   las1     <none>           <none>
pytest-worker-0   0/1     Completed           0            36s   192.168.221.177   las1     <none>           <none>
pytest-worker-0   0/1     Completed           0            36s   192.168.221.177   las1     <none>           <none>
pytest-worker-1   0/1     Completed           0            37s   192.168.221.152   las1     <none>           <none>
pytest-worker-2   0/1     Completed           0            37s   192.168.221.162   las1     <none>           <none>
pytest-worker-1   0/1     Completed           0            38s   192.168.221.152   las1     <none>           <none>
pytest-worker-2   0/1     Completed           0            38s   192.168.221.162   las1     <none>           <none>
pytest-worker-1   0/1     Completed           0            38s   192.168.221.152   las1     <none>           <none>
pytest-worker-2   0/1     Completed           0            38s   192.168.221.162   las1     <none>           <none>
pytest-master-0   0/1     Error               1 (32s ago)   64s   192.168.221.140   las1     <none>           <none>
pytest-master-0   0/1     CrashLoopBackOff    1 (15s ago)   77s   192.168.221.140   las1     <none>           <none>
pytest-master-0   1/1     Running             2 (16s ago)   78s   192.168.221.140   las1     <none>           <none>
pytest-master-0   0/1     Error               2 (46s ago)   108s   192.168.221.140   las1     <none>           <none>
pytest-master-0   0/1     CrashLoopBackOff    2 (16s ago)   2m3s   192.168.221.140   las1     <none>           <none>
pytest-master-0   1/1     Running             3 (28s ago)   2m15s   192.168.221.140   las1     <none>           <none>
pytest-master-0   1/1     Terminating         3 (28s ago)   2m15s   192.168.221.140   las1     <none>           <none>
pytest-worker-0   0/1     Completed           0             2m15s   192.168.221.177   las1     <none>           <none>
pytest-worker-0   0/1     Completed           0             2m15s   192.168.221.177   las1     <none>           <none>
pytest-worker-1   0/1     Completed           0             2m15s   192.168.221.152   las1     <none>           <none>
pytest-worker-1   0/1     Completed           0             2m15s   192.168.221.152   las1     <none>           <none>
pytest-worker-2   0/1     Completed           0             2m15s   192.168.221.162   las1     <none>           <none>
pytest-worker-2   0/1     Completed           0             2m15s   192.168.221.162   las1     <none>           <none>
pytest-master-0   1/1     Terminating         3 (29s ago)   2m16s   192.168.221.140   las1     <none>           <none>
pytest-master-0   0/1     Error               3 (29s ago)   2m16s   192.168.221.140   las1     <none>           <none>
pytest-master-0   0/1     Error               3 (30s ago)   2m17s   192.168.221.140   las1     <none>           <none>
pytest-master-0   0/1     Error               3 (30s ago)   2m17s   192.168.221.140   las1     <none>           <none>
```

可以看到 Master 失败后被重启，PyTorchJob 状态保持为 Running. 在 Master 重启 `spec.runPolicy.backoffLimit` 次仍然失败后，PyTorchJob 状态才变为 Failed. 此时进一步检查可发现 Pod 和 PodGroup 都被删除。

### Pod 被删除情形

经过实验可知 Pod 被删除的情形与 Pod 失败的情形类似，不同点在于重新拉起的 Pod 其 RESTARTS 初始化为 0, 所以 Master 被删除重启的次数没有限制。

## 结论

PyTorchJob 的状态基本跟随 Master Pod 的状态，例外情况：

- 当 Master 失败重启时，PyTorchJob 保持 Running 状态，直到 Master 不再重启且状态为失败
- 当所有 Worker 失败时，PyTorchJob 变为 Failed
