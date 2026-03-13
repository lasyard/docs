# 关于 activeDeadlineSeconds 的实验

Kubeflow Job 可以设置 `.spec.runPolicy.activeDeadlineSeconds`, 当 Job 的寿命大于指定的时间且未完成或失败时，将主动终止 Job 并将状态设为失败。这一逻辑体现在源码 <https://github.com/kubeflow/trainer/blob/release-1.9/pkg/controller.v1/common/job.go#L216> 处。但是由于以上代码在 `ReconcileJob` 函数中，如果系统不触发 `ReconcileJob`, 相关代码均不生效。

以 PyTorchJob 为例进行实验。PyTorchJob 定义：

:::{literalinclude} /_files/macos/workspace/k8s/kubeflow/pytorchjob.yaml
:::

## 生效情形

设置 `activeDeadlineSeconds` 时间小于作业运行时间 (30s)，提交：

```console
$ yq '.spec.runPolicy.activeDeadlineSeconds = 5' pytorchjob.yaml | kubectl apply -f -
```

监视 PyTorchJob 状态变化：

```console
$ kubectl get pytorchjob -owide -w
NAME     STATE   AGE
pytest           0s
pytest   Created   0s
pytest   Created   0s
pytest   Running   3s
pytest   Failed    6s
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
pytest-worker-1   0/1     Pending   0          1s    <none>   las1     <none>           <none>
pytest-worker-0   0/1     Pending   0          1s    <none>   las1     <none>           <none>
pytest-master-0   0/1     Pending   0          1s    <none>   las1     <none>           <none>
pytest-worker-2   0/1     Init:0/1   0          1s    <none>   las1     <none>           <none>
pytest-master-0   0/1     ContainerCreating   0          1s    <none>   las1     <none>           <none>
pytest-worker-0   0/1     Init:0/1            0          1s    <none>   las1     <none>           <none>
pytest-worker-1   0/1     Init:0/1            0          1s    <none>   las1     <none>           <none>
pytest-worker-2   0/1     Init:0/1            0          2s    <none>   las1     <none>           <none>
pytest-worker-0   0/1     Init:0/1            0          2s    <none>   las1     <none>           <none>
pytest-master-0   0/1     ContainerCreating   0          2s    <none>   las1     <none>           <none>
pytest-worker-1   0/1     Init:0/1            0          2s    <none>   las1     <none>           <none>
pytest-worker-1   0/1     Init:0/1            0          2s    192.168.221.145   las1     <none>           <none>
pytest-worker-2   0/1     Init:0/1            0          3s    192.168.221.144   las1     <none>           <none>
pytest-master-0   1/1     Running             0          3s    192.168.221.188   las1     <none>           <none>
pytest-worker-0   0/1     Init:0/1            0          3s    192.168.221.150   las1     <none>           <none>
pytest-worker-0   0/1     PodInitializing     0          5s    192.168.221.150   las1     <none>           <none>
pytest-master-0   1/1     Terminating         0          6s    192.168.221.188   las1     <none>           <none>
pytest-worker-1   0/1     PodInitializing     0          6s    192.168.221.145   las1     <none>           <none>
pytest-worker-2   0/1     PodInitializing     0          6s    192.168.221.144   las1     <none>           <none>
pytest-worker-0   0/1     Terminating         0          6s    192.168.221.150   las1     <none>           <none>
pytest-worker-1   0/1     Terminating         0          6s    192.168.221.145   las1     <none>           <none>
pytest-worker-2   0/1     Terminating         0          6s    192.168.221.144   las1     <none>           <none>
pytest-master-0   1/1     Terminating         0          6s    192.168.221.188   las1     <none>           <none>
pytest-master-0   0/1     Error               0          6s    192.168.221.188   las1     <none>           <none>
pytest-worker-1   1/1     Terminating         0          7s    192.168.221.145   las1     <none>           <none>
pytest-worker-0   1/1     Terminating         0          7s    192.168.221.150   las1     <none>           <none>
pytest-worker-2   1/1     Terminating         0          7s    192.168.221.144   las1     <none>           <none>
pytest-master-0   0/1     Error               0          7s    192.168.221.188   las1     <none>           <none>
pytest-master-0   0/1     Error               0          7s    192.168.221.188   las1     <none>           <none>
pytest-worker-1   1/1     Terminating         0          7s    192.168.221.145   las1     <none>           <none>
pytest-worker-2   1/1     Terminating         0          7s    192.168.221.144   las1     <none>           <none>
pytest-worker-0   1/1     Terminating         0          7s    192.168.221.150   las1     <none>           <none>
pytest-worker-1   0/1     Error               0          7s    192.168.221.145   las1     <none>           <none>
pytest-worker-2   0/1     Error               0          7s    192.168.221.144   las1     <none>           <none>
pytest-worker-0   0/1     Error               0          7s    192.168.221.150   las1     <none>           <none>
pytest-worker-1   0/1     Error               0          8s    192.168.221.145   las1     <none>           <none>
pytest-worker-1   0/1     Error               0          8s    192.168.221.145   las1     <none>           <none>
pytest-worker-2   0/1     Error               0          8s    192.168.221.144   las1     <none>           <none>
pytest-worker-2   0/1     Error               0          8s    192.168.221.144   las1     <none>           <none>
pytest-worker-0   0/1     Error               0          8s    192.168.221.150   las1     <none>           <none>
pytest-worker-0   0/1     Error               0          8s    192.168.221.150   las1     <none>           <none>
```

可见相关代码生效，及时停止了 Job. 这是因为相关的 Pod 状态仍在变化中，触发了 reconcileJob 操作。

## 不生效情形

设置 `activeDeadlineSeconds` 时间足够长使得所有 Pod 都进入稳定的 Running 状态：

```console
$ yq '.spec.runPolicy.activeDeadlineSeconds = 15' pytorchjob.yaml | kubectl apply -f -
```

监视 PyTorchJob 状态变化：

```console
$ kubectl get pytorchjob -owide -w
NAME     STATE   AGE
pytest           0s
pytest   Created   0s
pytest   Created   0s
pytest   Running   3s
pytest   Running   6s
pytest   Running   6s
pytest   Running   7s
pytest   Failed    33s
```

监视 Pod 状态变化：

```console
$ kubectl get po -owide -w
NAME              READY   STATUS    RESTARTS   AGE   IP       NODE     NOMINATED NODE   READINESS GATES
pytest-worker-0   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
pytest-worker-1   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
pytest-worker-2   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
pytest-master-0   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
pytest-worker-2   0/1     Pending   0          1s    <none>   las1     <none>           <none>
pytest-worker-1   0/1     Pending   0          1s    <none>   las1     <none>           <none>
pytest-master-0   0/1     Pending   0          1s    <none>   las1     <none>           <none>
pytest-worker-0   0/1     Pending   0          1s    <none>   las1     <none>           <none>
pytest-worker-2   0/1     Init:0/1   0          1s    <none>   las1     <none>           <none>
pytest-worker-1   0/1     Init:0/1   0          1s    <none>   las1     <none>           <none>
pytest-worker-0   0/1     Init:0/1   0          1s    <none>   las1     <none>           <none>
pytest-master-0   0/1     ContainerCreating   0          1s    <none>   las1     <none>           <none>
pytest-worker-2   0/1     Init:0/1            0          2s    <none>   las1     <none>           <none>
pytest-worker-1   0/1     Init:0/1            0          2s    <none>   las1     <none>           <none>
pytest-master-0   0/1     ContainerCreating   0          2s    <none>   las1     <none>           <none>
pytest-worker-0   0/1     Init:0/1            0          2s    <none>   las1     <none>           <none>
pytest-master-0   1/1     Running             0          3s    192.168.221.159   las1     <none>           <none>
pytest-worker-1   0/1     Init:0/1            0          3s    192.168.221.161   las1     <none>           <none>
pytest-worker-0   0/1     Init:0/1            0          3s    192.168.221.129   las1     <none>           <none>
pytest-worker-2   0/1     Init:0/1            0          3s    192.168.221.148   las1     <none>           <none>
pytest-worker-2   0/1     PodInitializing     0          5s    192.168.221.148   las1     <none>           <none>
pytest-worker-1   0/1     PodInitializing     0          5s    192.168.221.161   las1     <none>           <none>
pytest-worker-0   0/1     PodInitializing     0          6s    192.168.221.129   las1     <none>           <none>
pytest-worker-1   1/1     Running             0          6s    192.168.221.161   las1     <none>           <none>
pytest-worker-2   1/1     Running             0          6s    192.168.221.148   las1     <none>           <none>
pytest-worker-0   1/1     Running             0          7s    192.168.221.129   las1     <none>           <none>
pytest-master-0   0/1     Completed           0          33s   192.168.221.159   las1     <none>           <none>
pytest-worker-2   1/1     Terminating         0          33s   192.168.221.148   las1     <none>           <none>
pytest-master-0   0/1     Terminating         0          33s   192.168.221.159   las1     <none>           <none>
pytest-worker-0   1/1     Terminating         0          33s   192.168.221.129   las1     <none>           <none>
pytest-worker-1   1/1     Terminating         0          33s   192.168.221.161   las1     <none>           <none>
pytest-worker-0   1/1     Terminating         0          33s   192.168.221.129   las1     <none>           <none>
pytest-worker-2   1/1     Terminating         0          33s   192.168.221.148   las1     <none>           <none>
pytest-worker-1   1/1     Terminating         0          33s   192.168.221.161   las1     <none>           <none>
pytest-worker-2   0/1     Error               0          33s   192.168.221.148   las1     <none>           <none>
pytest-worker-0   0/1     Error               0          33s   192.168.221.129   las1     <none>           <none>
pytest-worker-1   0/1     Error               0          33s   192.168.221.161   las1     <none>           <none>
pytest-worker-1   0/1     Error               0          34s   192.168.221.161   las1     <none>           <none>
pytest-worker-1   0/1     Error               0          34s   192.168.221.161   las1     <none>           <none>
pytest-worker-0   0/1     Error               0          34s   192.168.221.129   las1     <none>           <none>
pytest-worker-0   0/1     Error               0          34s   192.168.221.129   las1     <none>           <none>
pytest-worker-2   0/1     Error               0          34s   192.168.221.148   las1     <none>           <none>
pytest-worker-2   0/1     Error               0          34s   192.168.221.148   las1     <none>           <none>
pytest-master-0   0/1     Terminating         0          34s   192.168.221.159   las1     <none>           <none>
pytest-master-0   0/1     Completed           0          34s   192.168.221.159   las1     <none>           <none>
pytest-master-0   0/1     Completed           0          35s   192.168.221.159   las1     <none>           <none>
pytest-master-0   0/1     Completed           0          35s   192.168.221.159   las1     <none>           <none>
```

可见因为没有状态变化，到达预定时间时，Job 并没有被取消，而是当有 Pod 状态变化时才发现 Job 已超时。

以上结果均已排除节点间时间不同步的状况。
