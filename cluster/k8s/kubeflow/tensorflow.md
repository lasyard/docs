# Kubeflow TFJob 调度实验

## 实验内容

TFJob 基本配置：

:::{literalinclude} /_files/macos/workspace/k8s/kubeflow/tfjob.yaml
:::

### 正常情况

提交以上 TFJob:

```console
$ kubectl apply -f tfjob.yaml
tfjob.kubeflow.org/tftest created
```

监视 TFJob 状态变化：

```console
$ kubectl get tfjob -owide -w
NAME     STATE   AGE
tftest           0s
tftest   Created   0s
tftest   Created   1s
tftest   Running   3s
tftest   Running   3s
tftest   Running   34s
tftest   Running   34s
tftest   Running   35s
tftest   Succeeded   35s
```

监视 PodGroup 状态变化：

```console
$ kubectl get podgroup -owide -w
NAME     STATUS   MINMEMBER   RUNNINGS   AGE   QUEUE
tftest            4                      0s    default
tftest   Inqueue   4                      1s    default
tftest   Running   4                      2s    default
tftest   Running   4           4          4s    default
tftest   Running   4           1          35s   default
tftest   Running   4           1          35s   default
```

监视 Pod 状态变化：

```console
$ kubectl get po -owide -w
NAME          READY   STATUS    RESTARTS   AGE   IP       NODE     NOMINATED NODE   READINESS GATES
tftest-ps-0   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
tftest-worker-0   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
tftest-worker-1   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
tftest-worker-2   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
tftest-ps-0       0/1     Pending   0          1s    <none>   las1     <none>           <none>
tftest-worker-1   0/1     Pending   0          1s    <none>   las1     <none>           <none>
tftest-worker-2   0/1     Pending   0          1s    <none>   las1     <none>           <none>
tftest-worker-0   0/1     Pending   0          1s    <none>   las1     <none>           <none>
tftest-ps-0       0/1     ContainerCreating   0          1s    <none>   las1     <none>           <none>
tftest-worker-1   0/1     ContainerCreating   0          1s    <none>   las1     <none>           <none>
tftest-worker-2   0/1     ContainerCreating   0          1s    <none>   las1     <none>           <none>
tftest-worker-0   0/1     ContainerCreating   0          1s    <none>   las1     <none>           <none>
tftest-ps-0       0/1     ContainerCreating   0          1s    <none>   las1     <none>           <none>
tftest-worker-1   0/1     ContainerCreating   0          1s    <none>   las1     <none>           <none>
tftest-worker-2   0/1     ContainerCreating   0          1s    <none>   las1     <none>           <none>
tftest-worker-0   0/1     ContainerCreating   0          2s    <none>   las1     <none>           <none>
tftest-worker-0   1/1     Running             0          2s    192.168.221.190   las1     <none>           <none>
tftest-worker-1   1/1     Running             0          2s    192.168.221.181   las1     <none>           <none>
tftest-worker-2   1/1     Running             0          2s    192.168.221.134   las1     <none>           <none>
tftest-ps-0       1/1     Running             0          2s    192.168.221.179   las1     <none>           <none>
tftest-ps-0       0/1     Completed           0          32s   192.168.221.179   las1     <none>           <none>
tftest-worker-2   0/1     Completed           0          32s   192.168.221.134   las1     <none>           <none>
tftest-worker-1   0/1     Completed           0          32s   192.168.221.181   las1     <none>           <none>
tftest-worker-0   0/1     Completed           0          33s   192.168.221.190   las1     <none>           <none>
tftest-ps-0       0/1     Completed           0          33s   192.168.221.179   las1     <none>           <none>
tftest-worker-2   0/1     Completed           0          33s   192.168.221.134   las1     <none>           <none>
tftest-worker-1   0/1     Completed           0          33s   192.168.221.181   las1     <none>           <none>
tftest-ps-0       0/1     Completed           0          33s   192.168.221.179   las1     <none>           <none>
tftest-worker-2   0/1     Completed           0          33s   192.168.221.134   las1     <none>           <none>
tftest-worker-1   0/1     Completed           0          34s   192.168.221.181   las1     <none>           <none>
tftest-worker-0   0/1     Completed           0          34s   192.168.221.190   las1     <none>           <none>
tftest-worker-0   0/1     Completed           0          34s   192.168.221.190   las1     <none>           <none>
```

可以观察到作业启动时创建了一个与 TFJob 同名的 PodGroup 且 `minMember` 被设置为 PS 与 Worker 的副本数之和。另外，由于 binpack 策略的存在，所有 Pod 被放在了同一个节点上。进一步观察可知 TFJob 成功后，PodGroup 被删除，Pod 仍存在。

另外可以观察到，TFJob 的状态变为 Running 是在所有 Worker 变为 Running 之后；同样的，状态变为 Succeeded 是在所有 Worker 变为 Completed 之后。初步得出结论，TFJob 的状态变化由所有 Worker 的状态决定。

PS 环境变量：

```console
$ kubectl describe po tftest-ps-0
...
    Environment:
      TF_CONFIG:  {"cluster":{"ps":["tftest-ps-0.default.svc:2222"],"worker":["tftest-worker-0.default.svc:2222","tftest-worker-1.default.svc:2222","tftest-worker-2.default.svc:2222"]},"task":{"type":"ps","index":0},"environment":"cloud"}
...
```

Worker 环境变量：

```console
...
$ kubectl describe po tftest-worker-0
    Environment:
      TF_CONFIG:  {"cluster":{"ps":["tftest-ps-0.default.svc:2222"],"worker":["tftest-worker-0.default.svc:2222","tftest-worker-1.default.svc:2222","tftest-worker-2.default.svc:2222"]},"task":{"type":"worker","index":0},"environment":"cloud"}
...
```

### 部分 Worker 失败情形

修改 TFJob 定义：

:::{literalinclude} /_files/macos/workspace/k8s/kubeflow/tfjob_fail_1_worker.yaml
:diff: /_files/macos/workspace/k8s/kubeflow/tfjob.yaml
:::

通过修改启动脚本人为使一个 Worker 失败。

提交作业后，监视 TFJob 状态变化：

```console
$ kubectl get tfjob -owide -w
NAME     STATE   AGE
tftest           0s
tftest   Created   0s
tftest   Created   1s
tftest   Running   3s
tftest   Running   3s
tftest   Running   3s
tftest   Running   4s
tftest   Running   34s
tftest   Running   34s
tftest   Failed    38s
```

监视 PodGroup 状态变化：

```console
$ kubectl get podgroup -owide -w
NAME     STATUS   MINMEMBER   RUNNINGS   AGE   QUEUE
tftest            4                      0s    default
tftest   Inqueue   4                      1s    default
tftest   Running   4                      2s    default
tftest   Running   4           3          4s    default
tftest   Running   4           4          5s    default
tftest   Running   4           2          35s   default
tftest   Running   4           2          38s   default
```

监视 Pod 状态变化：

```console
$ kubectl get po -owide -w
NAME          READY   STATUS    RESTARTS   AGE   IP       NODE     NOMINATED NODE   READINESS GATES
tftest-ps-0   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
tftest-worker-0   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
tftest-worker-1   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
tftest-worker-2   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
tftest-worker-2   0/1     Pending   0          1s    <none>   las1     <none>           <none>
tftest-worker-1   0/1     Pending   0          1s    <none>   las1     <none>           <none>
tftest-worker-0   0/1     Pending   0          1s    <none>   las1     <none>           <none>
tftest-ps-0       0/1     Pending   0          1s    <none>   las1     <none>           <none>
tftest-worker-2   0/1     ContainerCreating   0          1s    <none>   las1     <none>           <none>
tftest-worker-0   0/1     ContainerCreating   0          1s    <none>   las1     <none>           <none>
tftest-ps-0       0/1     ContainerCreating   0          1s    <none>   las1     <none>           <none>
tftest-worker-1   0/1     ContainerCreating   0          1s    <none>   las1     <none>           <none>
tftest-worker-2   0/1     ContainerCreating   0          1s    <none>   las1     <none>           <none>
tftest-worker-1   0/1     ContainerCreating   0          1s    <none>   las1     <none>           <none>
tftest-ps-0       0/1     ContainerCreating   0          1s    <none>   las1     <none>           <none>
tftest-worker-0   0/1     ContainerCreating   0          1s    <none>   las1     <none>           <none>
tftest-worker-1   1/1     Running             0          2s    192.168.221.162   las1     <none>           <none>
tftest-ps-0       1/1     Running             0          2s    192.168.221.152   las1     <none>           <none>
tftest-worker-2   1/1     Running             0          2s    192.168.221.177   las1     <none>           <none>
tftest-worker-0   1/1     Running             0          3s    192.168.221.140   las1     <none>           <none>
tftest-worker-0   0/1     Error               0          13s   192.168.221.140   las1     <none>           <none>
tftest-worker-0   1/1     Running             1 (3s ago)   14s   192.168.221.140   las1     <none>           <none>
tftest-worker-0   0/1     Error               1 (13s ago)   24s   192.168.221.140   las1     <none>           <none>
tftest-ps-0       0/1     Completed           0             32s   192.168.221.152   las1     <none>           <none>
tftest-worker-2   0/1     Completed           0             32s   192.168.221.177   las1     <none>           <none>
tftest-worker-1   0/1     Completed           0             32s   192.168.221.162   las1     <none>           <none>
tftest-ps-0       1/1     Running             1 (3s ago)    33s   192.168.221.152   las1     <none>           <none>
tftest-worker-1   0/1     Completed           0             33s   192.168.221.162   las1     <none>           <none>
tftest-worker-2   0/1     Completed           0             33s   192.168.221.177   las1     <none>           <none>
tftest-worker-1   0/1     Completed           0             33s   192.168.221.162   las1     <none>           <none>
tftest-worker-2   0/1     Completed           0             33s   192.168.221.177   las1     <none>           <none>
tftest-worker-0   0/1     CrashLoopBackOff    1 (14s ago)   36s   192.168.221.140   las1     <none>           <none>
tftest-worker-0   1/1     Running             2 (15s ago)   37s   192.168.221.140   las1     <none>           <none>
tftest-ps-0       1/1     Terminating         1 (7s ago)    37s   192.168.221.152   las1     <none>           <none>
tftest-worker-0   1/1     Terminating         2 (15s ago)   37s   192.168.221.140   las1     <none>           <none>
tftest-worker-1   0/1     Completed           0             37s   192.168.221.162   las1     <none>           <none>
tftest-worker-1   0/1     Completed           0             37s   192.168.221.162   las1     <none>           <none>
tftest-worker-2   0/1     Completed           0             37s   192.168.221.177   las1     <none>           <none>
tftest-worker-2   0/1     Completed           0             37s   192.168.221.177   las1     <none>           <none>
tftest-ps-0       1/1     Terminating         1 (7s ago)    37s   192.168.221.152   las1     <none>           <none>
tftest-ps-0       0/1     Error               1 (7s ago)    37s   192.168.221.152   las1     <none>           <none>
tftest-ps-0       0/1     Error               1 (8s ago)    38s   192.168.221.152   las1     <none>           <none>
tftest-ps-0       0/1     Error               1 (8s ago)    38s   192.168.221.152   las1     <none>           <none>
tftest-worker-0   1/1     Terminating         2 (16s ago)   38s   192.168.221.140   las1     <none>           <none>
tftest-worker-0   0/1     Error               2 (16s ago)   38s   192.168.221.140   las1     <none>           <none>
tftest-worker-0   0/1     Error               2 (17s ago)   39s   192.168.221.140   las1     <none>           <none>
tftest-worker-0   0/1     Error               2 (17s ago)   39s   192.168.221.140   las1     <none>           <none>
```

可见单个 Worker 失败将导致整个 TFJob 失败，然后所有 Pod 被清理。

### PS 失败情形

修改 TFJob 定义：

:::{literalinclude} /_files/macos/workspace/k8s/kubeflow/tfjob_fail_ps.yaml
:diff: /_files/macos/workspace/k8s/kubeflow/tfjob.yaml
:::

提交作业后，监视 TFJob 状态变化：

```console
$ kubectl get tfjob -owide -w
NAME     STATE   AGE
tftest           0s
tftest   Created   0s
tftest   Created   1s
tftest   Running   3s
tftest   Running   3s
tftest   Running   3s
tftest   Succeeded   35s
tftest   Succeeded   35s
```

监视 PodGroup 状态变化：

```console
$ kubectl get podgroup -owide -w
NAME     STATUS   MINMEMBER   RUNNINGS   AGE   QUEUE
tftest            4                      0s    default
tftest   Inqueue   4                      1s    default
tftest   Running   4                      2s    default
tftest   Running   4           4          4s    default
tftest   Running   4           4          35s   default
```

监视 Pod 状态变化：

```console
$ kubectl get po -owide -w
NAME              READY   STATUS    RESTARTS   AGE   IP       NODE     NOMINATED NODE   READINESS GATES
tftest-worker-0   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
tftest-worker-1   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
tftest-worker-2   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
tftest-ps-0       0/1     Pending   0          0s    <none>   <none>   <none>           <none>
tftest-worker-2   0/1     Pending   0          1s    <none>   las1     <none>           <none>
tftest-worker-1   0/1     Pending   0          1s    <none>   las1     <none>           <none>
tftest-worker-0   0/1     Pending   0          1s    <none>   las1     <none>           <none>
tftest-ps-0       0/1     Pending   0          1s    <none>   las1     <none>           <none>
tftest-worker-2   0/1     ContainerCreating   0          1s    <none>   las1     <none>           <none>
tftest-worker-1   0/1     ContainerCreating   0          1s    <none>   las1     <none>           <none>
tftest-worker-0   0/1     ContainerCreating   0          1s    <none>   las1     <none>           <none>
tftest-ps-0       0/1     ContainerCreating   0          1s    <none>   las1     <none>           <none>
tftest-worker-2   0/1     ContainerCreating   0          1s    <none>   las1     <none>           <none>
tftest-ps-0       0/1     ContainerCreating   0          1s    <none>   las1     <none>           <none>
tftest-worker-1   0/1     ContainerCreating   0          1s    <none>   las1     <none>           <none>
tftest-worker-0   0/1     ContainerCreating   0          1s    <none>   las1     <none>           <none>
tftest-worker-0   1/1     Running             0          2s    192.168.221.155   las1     <none>           <none>
tftest-worker-2   1/1     Running             0          2s    192.168.221.141   las1     <none>           <none>
tftest-ps-0       1/1     Running             0          2s    192.168.221.135   las1     <none>           <none>
tftest-worker-1   1/1     Running             0          2s    192.168.221.138   las1     <none>           <none>
tftest-ps-0       0/1     Error               0          17s   192.168.221.135   las1     <none>           <none>
tftest-ps-0       1/1     Running             1 (3s ago)   18s   192.168.221.135   las1     <none>           <none>
tftest-worker-0   0/1     Completed           0            32s   192.168.221.155   las1     <none>           <none>
tftest-worker-1   0/1     Completed           0            32s   192.168.221.138   las1     <none>           <none>
tftest-worker-2   0/1     Completed           0            33s   192.168.221.141   las1     <none>           <none>
tftest-ps-0       0/1     Error               1 (18s ago)   33s   192.168.221.135   las1     <none>           <none>
tftest-worker-0   0/1     Completed           0             34s   192.168.221.155   las1     <none>           <none>
tftest-worker-2   0/1     Completed           0             34s   192.168.221.141   las1     <none>           <none>
tftest-worker-1   0/1     Completed           0             34s   192.168.221.138   las1     <none>           <none>
tftest-worker-0   0/1     Completed           0             34s   192.168.221.155   las1     <none>           <none>
tftest-worker-1   0/1     Completed           0             34s   192.168.221.138   las1     <none>           <none>
tftest-worker-2   0/1     Completed           0             34s   192.168.221.141   las1     <none>           <none>
tftest-ps-0       0/1     CrashLoopBackOff    1 (13s ago)   44s   192.168.221.135   las1     <none>           <none>
tftest-ps-0       1/1     Running             2 (14s ago)   45s   192.168.221.135   las1     <none>           <none>
tftest-ps-0       0/1     Error               2 (29s ago)   60s   192.168.221.135   las1     <none>           <none>
tftest-ps-0       0/1     CrashLoopBackOff    2 (15s ago)   73s   192.168.221.135   las1     <none>           <none>
tftest-ps-0       1/1     Running             3 (31s ago)   89s   192.168.221.135   las1     <none>           <none>
tftest-ps-0       0/1     Error               3 (46s ago)   104s   192.168.221.135   las1     <none>           <none>
tftest-ps-0       0/1     CrashLoopBackOff    3 (16s ago)   118s   192.168.221.135   las1     <none>           <none>
tftest-ps-0       1/1     Running             4 (52s ago)   2m34s   192.168.221.135   las1     <none>           <none>
tftest-ps-0       0/1     Error               4 (67s ago)   2m49s   192.168.221.135   las1     <none>           <none>
tftest-ps-0       0/1     CrashLoopBackOff    4 (16s ago)   3m3s    192.168.221.135   las1     <none>           <none>
```

可见 PS 失败不影响 TFJob 的结果。由于 `restartPolicy` 为 `Always`, PS 失败以后不断重启且次数不受限制。

## 结论

TFJob 的状态与所有 Worker 的状态相关，只要有一个 Worker 失败，作业就失败。
