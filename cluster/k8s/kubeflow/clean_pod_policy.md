# 关于 cleanPodPolicy 的实验

## Pod 清理策略

Kubeflow V1 的作业有 `spec.runPolicy.cleanPodPolicy` 参数。默认情况下，当作业成功时，Pod 被保留；当作业失败时，Pod 被清理。

源码中 `CleanPodPolicy` 的定义在 <https://github.com/kubeflow/trainer/blob/release-1.9/pkg/apis/kubeflow.org/v1/common_types.go#L162>:

```go
// CleanPodPolicy describes how to deal with pods when the job is finished.
type CleanPodPolicy string

const (
    CleanPodPolicyUndefined CleanPodPolicy = ""
    CleanPodPolicyAll       CleanPodPolicy = "All"
    CleanPodPolicyRunning   CleanPodPolicy = "Running"
    CleanPodPolicyNone      CleanPodPolicy = "None"
)
```

清理 Pod 相关的代码在 <https://github.com/kubeflow/trainer/blob/release-1.9/pkg/controller.v1/common/job.go#L43> 函数 `DeletePodsAndServices` 中。

可见当作业结束时清理 Pod 的原则如下表：

| cleanPodPolicy | 动作                                 |
| -------------- | ------------------------------------ |
| `"None"`       | 不清理                               |
| `"Running"`    | 清理状态为 RUNNING 和 PENDING 的 Pod |
| `"All"`        | 全部清理                             |

默认策略为 `"None"`.

## 实验结果

试验将 `cleanPodPolicy` 设为 "All":

```console
$ yq eval '.spec.runPolicy.cleanPodPolicy = "All"' pytorchjob.yaml | kubectl apply -f -
```

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
kubectl get po -owide -w
NAME              READY   STATUS    RESTARTS   AGE   IP       NODE     NOMINATED NODE   READINESS GATES
pytest-worker-0   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
pytest-worker-1   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
pytest-worker-2   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
pytest-master-0   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
pytest-worker-0   0/1     Pending   0          1s    <none>   las1     <none>           <none>
pytest-worker-1   0/1     Pending   0          1s    <none>   las1     <none>           <none>
pytest-worker-2   0/1     Pending   0          1s    <none>   las1     <none>           <none>
pytest-master-0   0/1     Pending   0          1s    <none>   las1     <none>           <none>
pytest-worker-0   0/1     Init:0/1   0          1s    <none>   las1     <none>           <none>
pytest-worker-1   0/1     Init:0/1   0          1s    <none>   las1     <none>           <none>
pytest-worker-2   0/1     Init:0/1   0          1s    <none>   las1     <none>           <none>
pytest-master-0   0/1     ContainerCreating   0          1s    <none>   las1     <none>           <none>
pytest-worker-0   0/1     Init:0/1            0          1s    <none>   las1     <none>           <none>
pytest-worker-1   0/1     Init:0/1            0          1s    <none>   las1     <none>           <none>
pytest-worker-2   0/1     Init:0/1            0          2s    <none>   las1     <none>           <none>
pytest-master-0   0/1     ContainerCreating   0          2s    <none>   las1     <none>           <none>
pytest-master-0   1/1     Running             0          2s    192.168.221.178   las1     <none>           <none>
pytest-worker-2   0/1     Init:0/1            0          3s    192.168.221.142   las1     <none>           <none>
pytest-worker-0   0/1     Init:0/1            0          3s    192.168.221.172   las1     <none>           <none>
pytest-worker-1   0/1     Init:0/1            0          3s    192.168.221.166   las1     <none>           <none>
pytest-worker-2   0/1     PodInitializing     0          5s    192.168.221.142   las1     <none>           <none>
pytest-worker-0   0/1     PodInitializing     0          5s    192.168.221.172   las1     <none>           <none>
pytest-worker-1   0/1     PodInitializing     0          5s    192.168.221.166   las1     <none>           <none>
pytest-worker-0   1/1     Running             0          6s    192.168.221.172   las1     <none>           <none>
pytest-worker-1   1/1     Running             0          6s    192.168.221.166   las1     <none>           <none>
pytest-worker-2   1/1     Running             0          6s    192.168.221.142   las1     <none>           <none>
pytest-master-0   0/1     Completed           0          33s   192.168.221.178   las1     <none>           <none>
pytest-master-0   0/1     Completed           0          34s   192.168.221.178   las1     <none>           <none>
pytest-master-0   0/1     Completed           0          34s   192.168.221.178   las1     <none>           <none>
pytest-worker-1   1/1     Terminating         0          34s   192.168.221.166   las1     <none>           <none>
pytest-worker-2   1/1     Terminating         0          34s   192.168.221.142   las1     <none>           <none>
pytest-master-0   0/1     Completed           0          34s   192.168.221.178   las1     <none>           <none>
pytest-master-0   0/1     Completed           0          34s   192.168.221.178   las1     <none>           <none>
pytest-worker-0   1/1     Terminating         0          34s   192.168.221.172   las1     <none>           <none>
pytest-worker-1   1/1     Terminating         0          34s   192.168.221.166   las1     <none>           <none>
pytest-worker-2   1/1     Terminating         0          34s   192.168.221.142   las1     <none>           <none>
pytest-worker-0   1/1     Terminating         0          34s   192.168.221.172   las1     <none>           <none>
pytest-worker-1   0/1     Error               0          35s   192.168.221.166   las1     <none>           <none>
pytest-worker-2   0/1     Error               0          35s   192.168.221.142   las1     <none>           <none>
pytest-worker-0   0/1     Error               0          35s   192.168.221.172   las1     <none>           <none>
pytest-worker-1   0/1     Error               0          35s   192.168.221.166   las1     <none>           <none>
pytest-worker-1   0/1     Error               0          35s   192.168.221.166   las1     <none>           <none>
pytest-worker-0   0/1     Error               0          36s   192.168.221.172   las1     <none>           <none>
pytest-worker-0   0/1     Error               0          36s   192.168.221.172   las1     <none>           <none>
pytest-worker-2   0/1     Error               0          36s   192.168.221.142   las1     <none>           <none>
pytest-worker-2   0/1     Error               0          36s   192.168.221.142   las1     <none>           <none>
```

可见在 PyTorchJob 成功后对其他 Worker 发起了删除操作，这些 Worker 变成 Error 状态。可验证此时包括 Master 在内的 Pod 已经都不存在。

对于部分 Worker 失败情形，当 PyTorchJob 结束后，由于所有 Pod 被清理，不会发生 Worker 无限重启。

针对其他设置值的试验结果，当作业成功时与预期相同，当作业失败时，无论 `cleanPodPolicy` 设为何值，所有 Pod 均被删除。

从源码 <https://github.com/kubeflow/trainer/blob/release-1.9/pkg/controller.v1/common/job.go#L216> 可以看出，如果不设 `spec.runPolicy.backoffLimit`，那么失败以后的 Pod 清理是不生效的。

为了验证，去除这个设置重做 PyTorchJob 全部 Worker 失败的实验：

```console
$ yq 'del(.spec.runPolicy.backoffLimit)' pytorchjob_fail_all_workers.yaml | kubectl apply -f -
```

监视 PyTorchJob 状态变化：

```console
$ kubectl get pytorchjob -owide -w
NAME     STATE   AGE
pytest           0s
pytest   Created   0s
pytest   Created   0s
pytest   Running   2s
pytest   Running   6s
pytest   Running   6s
pytest   Running   6s
pytest   Succeeded   34s
pytest   Succeeded   34s
```

监视 Pod 状态变化：

```console
$ kubectl get po -owide -w
NAME              READY   STATUS    RESTARTS   AGE   IP       NODE     NOMINATED NODE   READINESS GATES
pytest-worker-0   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
pytest-worker-1   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
pytest-worker-2   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
pytest-master-0   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
pytest-worker-0   0/1     Pending   0          1s    <none>   las1     <none>           <none>
pytest-worker-1   0/1     Pending   0          1s    <none>   las1     <none>           <none>
pytest-master-0   0/1     Pending   0          1s    <none>   las1     <none>           <none>
pytest-worker-2   0/1     Pending   0          1s    <none>   las1     <none>           <none>
pytest-worker-0   0/1     Init:0/1   0          1s    <none>   las1     <none>           <none>
pytest-worker-1   0/1     Init:0/1   0          1s    <none>   las1     <none>           <none>
pytest-master-0   0/1     ContainerCreating   0          1s    <none>   las1     <none>           <none>
pytest-worker-2   0/1     Init:0/1            0          1s    <none>   las1     <none>           <none>
pytest-worker-0   0/1     Init:0/1            0          2s    <none>   las1     <none>           <none>
pytest-master-0   0/1     ContainerCreating   0          2s    <none>   las1     <none>           <none>
pytest-worker-1   0/1     Init:0/1            0          2s    <none>   las1     <none>           <none>
pytest-worker-2   0/1     Init:0/1            0          2s    <none>   las1     <none>           <none>
pytest-worker-2   0/1     Init:0/1            0          2s    192.168.221.182   las1     <none>           <none>
pytest-worker-1   0/1     Init:0/1            0          2s    192.168.221.148   las1     <none>           <none>
pytest-worker-0   0/1     Init:0/1            0          2s    192.168.221.180   las1     <none>           <none>
pytest-master-0   1/1     Running             0          2s    192.168.221.137   las1     <none>           <none>
pytest-worker-2   0/1     PodInitializing     0          5s    192.168.221.182   las1     <none>           <none>
pytest-worker-0   0/1     PodInitializing     0          5s    192.168.221.180   las1     <none>           <none>
pytest-worker-1   0/1     PodInitializing     0          5s    192.168.221.148   las1     <none>           <none>
pytest-worker-0   1/1     Running             0          6s    192.168.221.180   las1     <none>           <none>
pytest-worker-1   1/1     Running             0          6s    192.168.221.148   las1     <none>           <none>
pytest-worker-2   1/1     Running             0          6s    192.168.221.182   las1     <none>           <none>
pytest-worker-0   0/1     Error               0          16s   192.168.221.180   las1     <none>           <none>
pytest-worker-1   0/1     Error               0          16s   192.168.221.148   las1     <none>           <none>
pytest-worker-2   0/1     Error               0          16s   192.168.221.182   las1     <none>           <none>
pytest-worker-0   1/1     Running             1 (2s ago)   17s   192.168.221.180   las1     <none>           <none>
pytest-worker-1   1/1     Running             1 (2s ago)   17s   192.168.221.148   las1     <none>           <none>
pytest-worker-2   1/1     Running             1 (2s ago)   17s   192.168.221.182   las1     <none>           <none>
pytest-worker-0   0/1     Error               1 (12s ago)   27s   192.168.221.180   las1     <none>           <none>
pytest-worker-1   0/1     Error               1 (13s ago)   28s   192.168.221.148   las1     <none>           <none>
pytest-worker-2   0/1     Error               1 (13s ago)   28s   192.168.221.182   las1     <none>           <none>
pytest-master-0   0/1     Completed           0             33s   192.168.221.137   las1     <none>           <none>
pytest-master-0   0/1     Completed           0             34s   192.168.221.137   las1     <none>           <none>
pytest-master-0   0/1     Completed           0             34s   192.168.221.137   las1     <none>           <none>
pytest-worker-0   0/1     CrashLoopBackOff    1 (13s ago)   39s   192.168.221.180   las1     <none>           <none>
pytest-worker-0   1/1     Running             2 (14s ago)   40s   192.168.221.180   las1     <none>           <none>
pytest-worker-1   0/1     CrashLoopBackOff    1 (16s ago)   42s   192.168.221.148   las1     <none>           <none>
pytest-worker-2   0/1     CrashLoopBackOff    1 (16s ago)   42s   192.168.221.182   las1     <none>           <none>
pytest-worker-1   1/1     Running             2 (17s ago)   43s   192.168.221.148   las1     <none>           <none>
pytest-worker-2   1/1     Running             2 (17s ago)   43s   192.168.221.182   las1     <none>           <none>
pytest-worker-0   0/1     Error               2 (24s ago)   50s   192.168.221.180   las1     <none>           <none>
pytest-worker-1   0/1     Error               2 (27s ago)   53s   192.168.221.148   las1     <none>           <none>
pytest-worker-2   0/1     Error               2 (27s ago)   53s   192.168.221.182   las1     <none>           <none>
pytest-worker-0   0/1     CrashLoopBackOff    2 (16s ago)   64s   192.168.221.180   las1     <none>           <none>
pytest-worker-1   0/1     CrashLoopBackOff    2 (13s ago)   64s   192.168.221.148   las1     <none>           <none>
pytest-worker-2   0/1     CrashLoopBackOff    2 (15s ago)   66s   192.168.221.182   las1     <none>           <none>
pytest-worker-1   1/1     Running             3 (25s ago)   76s   192.168.221.148   las1     <none>           <none>
pytest-worker-0   1/1     Running             3 (30s ago)   78s   192.168.221.180   las1     <none>           <none>
pytest-worker-2   1/1     Running             3 (29s ago)   80s   192.168.221.182   las1     <none>           <none>
pytest-worker-1   0/1     Error               3 (35s ago)   86s   192.168.221.148   las1     <none>           <none>
pytest-worker-0   0/1     Error               3 (40s ago)   88s   192.168.221.180   las1     <none>           <none>
pytest-worker-2   0/1     Error               3 (39s ago)   90s   192.168.221.182   las1     <none>           <none>
pytest-worker-1   0/1     CrashLoopBackOff    3 (14s ago)   98s   192.168.221.148   las1     <none>           <none>
pytest-worker-0   0/1     CrashLoopBackOff    3 (14s ago)   100s   192.168.221.180   las1     <none>           <none>
pytest-worker-2   0/1     CrashLoopBackOff    3 (14s ago)   102s   192.168.221.182   las1     <none>           <none>
pytest-worker-0   1/1     Running             4 (43s ago)   2m9s   192.168.221.180   las1     <none>           <none>
pytest-worker-1   1/1     Running             4 (53s ago)   2m17s   192.168.221.148   las1     <none>           <none>
pytest-worker-0   0/1     Error               4 (53s ago)   2m19s   192.168.221.180   las1     <none>           <none>
pytest-worker-2   1/1     Running             4 (56s ago)   2m24s   192.168.221.182   las1     <none>           <none>
pytest-worker-1   0/1     Error               4 (63s ago)   2m27s   192.168.221.148   las1     <none>           <none>
pytest-worker-0   0/1     CrashLoopBackOff    4 (13s ago)   2m30s   192.168.221.180   las1     <none>           <none>
pytest-worker-2   0/1     Error               4 (66s ago)   2m34s   192.168.221.182   las1     <none>           <none>
pytest-worker-1   0/1     CrashLoopBackOff    4 (17s ago)   2m42s   192.168.221.148   las1     <none>           <none>
pytest-worker-2   0/1     CrashLoopBackOff    4 (13s ago)   2m45s   192.168.221.182   las1     <none>           <none>
```

可以看出，这种情况下失败的 Pod 没有被清理，进入了无限重启，而且作业的状态竟然变成了 Succeeded. 综合考虑，似乎将默认 `backoffLimit` 设为 `0` 更合理。
