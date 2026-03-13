# 关于 restartPolicy 为 ExitCode 的实验

PyTorchJob 的 Master 和 Worker, TFJob 的 PS 和 Worker 都可以设置 `restartPolicy`. 关于其取值，引用 [Kubeflow 官方文档](https://v1-9-branch.kubeflow.org/docs/components/training/user-guides/tensorflow/) 的说明：

> `restartPolicy` Determines whether pods will be restarted when they exit. The allowed values are as follows
>
> - `Always` means the pod will always be restarted. This policy is good for parameter servers since they never exit and should always be restarted in the event of failure.
> - `OnFailure` means the pod will be restarted if the pod exits due to failure.
>   - A non-zero exit code indicates a failure.
>   - An exit code of 0 indicates success and the pod will not be restarted.
>   - This policy is good for chief and workers.
> - `ExitCode` means the restart behavior is dependent on the exit code of the tensorflow container as follows:
>   - Exit code 0 indicates the process completed successfully and will not be restarted.
>   - The following exit codes indicate a permanent error and the container will not be restarted:
>     - 1: general errors
>     - 2: misuse of shell builtins
>     - 126: command invoked cannot execute
>     - 127: command not found
>     - 128: invalid argument to exit
>     - 139: container terminated by SIGSEGV (invalid memory reference)
>   - The following exit codes indicate a retryable error and the container will be restarted:
>     - 130: container terminated by SIGINT (keyboard Control-C)
>     - 137: container received a SIGKILL
>     - 143: container received a SIGTERM
>   - Exit code 138 corresponds to SIGUSR1 and is reserved for user-specified retryable errors.
>   - Other exit codes are undefined and there is no guarantee about the behavior.
> - `Never` means pods that terminate will never be restarted. This policy should rarely be used because Kubernetes will terminate pods for any number of reasons (e.g. node becomes unhealthy) and this will prevent the job from recovering.

这里 `Always`, `OnFailure`, `Never` 都是在 Pod 层面上由 Kubernetes 本身实现的，而 `ExitCode` 在 Pod 层面上没有实现，是由 Kubeflow training operator 实现的。下面的实验说明了这一点。

TFJob 的定义：

:::{literalinclude} /_files/macos/workspace/k8s/kubeflow/tfjob_fail_exit_code.yaml
:::

利用脚本使一个 Worker 失败且返回 138, 这将导致 Pod 重启。

提交作业后，监视 TFJob 状态变化：

```console
$ kubectl get tfjob -owide -w
NAME     STATE   AGE
tftest           0s
tftest   Created   0s
tftest   Created   0s
tftest   Running   2s
tftest   Running   2s
tftest   Running   3s
tftest   Running   3s
tftest   Restarting   15s
tftest   Running      15s
tftest   Running      16s
tftest   Restarting   28s
tftest   Running      28s
tftest   Running      29s
tftest   Running      34s
tftest   Running      34s
tftest   Running      35s
tftest   Restarting   41s
tftest   Restarting   41s
tftest   Running      42s
tftest   Restarting   54s
tftest   Restarting   54s
tftest   Running      55s
```

监视 PodGroup 状态变化：

```console
$ kubectl get podgroup -owide -w
NAME     STATUS   MINMEMBER   RUNNINGS   AGE   QUEUE
tftest            4                      0s    default
tftest   Inqueue   4                      0s    default
tftest   Running   4                      1s    default
tftest   Running   4           2          2s    default
tftest   Running   4           4          3s    default
tftest   Running   4           3          15s   default
tftest   Running   4           4          16s   default
tftest   Running   4           3          28s   default
tftest   Running   4           4          29s   default
tftest   Running   4           2          34s   default
tftest   Running   4           1          35s   default
tftest   Running   4                      42s   default
tftest   Running   4           1          43s   default
tftest   Running   4                      55s   default
tftest   Running   4           1          56s   default
```

监视 Pod 状态变化：

```console
$ kubectl get po -owide -w
NAME          READY   STATUS    RESTARTS   AGE   IP       NODE     NOMINATED NODE   READINESS GATES
tftest-ps-0   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
tftest-worker-0   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
tftest-worker-1   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
tftest-worker-2   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
tftest-worker-0   0/1     Pending   0          1s    <none>   las1     <none>           <none>
tftest-worker-2   0/1     Pending   0          1s    <none>   las1     <none>           <none>
tftest-worker-1   0/1     Pending   0          1s    <none>   las1     <none>           <none>
tftest-ps-0       0/1     Pending   0          1s    <none>   las1     <none>           <none>
tftest-worker-0   0/1     ContainerCreating   0          1s    <none>   las1     <none>           <none>
tftest-worker-2   0/1     ContainerCreating   0          1s    <none>   las1     <none>           <none>
tftest-worker-1   0/1     ContainerCreating   0          1s    <none>   las1     <none>           <none>
tftest-ps-0       0/1     ContainerCreating   0          1s    <none>   las1     <none>           <none>
tftest-worker-0   0/1     ContainerCreating   0          2s    <none>   las1     <none>           <none>
tftest-worker-2   0/1     ContainerCreating   0          2s    <none>   las1     <none>           <none>
tftest-worker-1   0/1     ContainerCreating   0          2s    <none>   las1     <none>           <none>
tftest-ps-0       0/1     ContainerCreating   0          2s    <none>   las1     <none>           <none>
tftest-worker-0   1/1     Running             0          2s    192.168.221.129   las1     <none>           <none>
tftest-worker-2   1/1     Running             0          2s    192.168.221.184   las1     <none>           <none>
tftest-ps-0       1/1     Running             0          3s    192.168.221.137   las1     <none>           <none>
tftest-worker-1   1/1     Running             0          3s    192.168.221.183   las1     <none>           <none>
tftest-worker-0   0/1     Error               0          13s   192.168.221.129   las1     <none>           <none>
tftest-worker-0   0/1     Error               0          14s   192.168.221.129   las1     <none>           <none>
tftest-worker-0   0/1     Error               0          15s   192.168.221.129   las1     <none>           <none>
tftest-worker-0   0/1     Error               0          15s   192.168.221.129   las1     <none>           <none>
tftest-worker-0   0/1     Error               0          15s   192.168.221.129   las1     <none>           <none>
tftest-worker-0   0/1     Pending             0          0s    <none>            <none>   <none>           <none>
tftest-worker-0   0/1     Pending             0          0s    <none>            las1     <none>           <none>
tftest-worker-0   0/1     ContainerCreating   0          0s    <none>            las1     <none>           <none>
tftest-worker-0   0/1     ContainerCreating   0          1s    <none>            las1     <none>           <none>
tftest-worker-0   1/1     Running             0          1s    192.168.221.148   las1     <none>           <none>
tftest-worker-0   0/1     Error               0          11s   192.168.221.148   las1     <none>           <none>
tftest-worker-0   0/1     Error               0          12s   192.168.221.148   las1     <none>           <none>
tftest-worker-0   0/1     Error               0          13s   192.168.221.148   las1     <none>           <none>
tftest-worker-0   0/1     Error               0          13s   192.168.221.148   las1     <none>           <none>
tftest-worker-0   0/1     Error               0          13s   192.168.221.148   las1     <none>           <none>
tftest-worker-0   0/1     Pending             0          0s    <none>            <none>   <none>           <none>
tftest-worker-0   0/1     Pending             0          0s    <none>            las1     <none>           <none>
tftest-worker-0   0/1     ContainerCreating   0          0s    <none>            las1     <none>           <none>
tftest-worker-0   0/1     ContainerCreating   0          1s    <none>            las1     <none>           <none>
tftest-worker-0   1/1     Running             0          1s    192.168.221.180   las1     <none>           <none>
tftest-worker-2   0/1     Completed           0          32s   192.168.221.184   las1     <none>           <none>
tftest-worker-1   0/1     Completed           0          32s   192.168.221.183   las1     <none>           <none>
tftest-ps-0       0/1     Completed           0          33s   192.168.221.137   las1     <none>           <none>
tftest-worker-2   0/1     Completed           0          34s   192.168.221.184   las1     <none>           <none>
tftest-worker-1   0/1     Completed           0          34s   192.168.221.183   las1     <none>           <none>
tftest-worker-2   0/1     Completed           0          34s   192.168.221.184   las1     <none>           <none>
tftest-worker-1   0/1     Completed           0          34s   192.168.221.183   las1     <none>           <none>
tftest-ps-0       0/1     Completed           0          35s   192.168.221.137   las1     <none>           <none>
tftest-ps-0       0/1     Completed           0          35s   192.168.221.137   las1     <none>           <none>
tftest-worker-0   0/1     Error               0          11s   192.168.221.180   las1     <none>           <none>
tftest-worker-0   0/1     Error               0          12s   192.168.221.180   las1     <none>           <none>
tftest-worker-0   0/1     Error               0          13s   192.168.221.180   las1     <none>           <none>
tftest-worker-0   0/1     Error               0          13s   192.168.221.180   las1     <none>           <none>
tftest-worker-0   0/1     Error               0          13s   192.168.221.180   las1     <none>           <none>
tftest-worker-0   0/1     Pending             0          0s    <none>            <none>   <none>           <none>
tftest-worker-0   0/1     Pending             0          1s    <none>            las1     <none>           <none>
tftest-worker-0   0/1     ContainerCreating   0          1s    <none>            las1     <none>           <none>
tftest-worker-0   0/1     ContainerCreating   0          1s    <none>            las1     <none>           <none>
tftest-worker-0   1/1     Running             0          1s    192.168.221.182   las1     <none>           <none>
tftest-worker-0   0/1     Error               0          11s   192.168.221.182   las1     <none>           <none>
tftest-worker-0   0/1     Error               0          13s   192.168.221.182   las1     <none>           <none>
tftest-worker-0   0/1     Error               0          13s   192.168.221.182   las1     <none>           <none>
tftest-worker-0   0/1     Error               0          13s   192.168.221.182   las1     <none>           <none>
tftest-worker-0   0/1     Error               0          13s   192.168.221.182   las1     <none>           <none>
tftest-worker-0   0/1     Pending             0          0s    <none>            <none>   <none>           <none>
tftest-worker-0   0/1     Pending             0          1s    <none>            las1     <none>           <none>
tftest-worker-0   0/1     ContainerCreating   0          1s    <none>            las1     <none>           <none>
tftest-worker-0   0/1     ContainerCreating   0          1s    <none>            las1     <none>           <none>
tftest-worker-0   1/1     Running             0          1s    192.168.221.130   las1     <none>           <none>
tftest-worker-0   0/1     Error               0          11s   192.168.221.130   las1     <none>           <none>
```

与 `restartPolicy` 设置为 `OnFailure` 时相比，当一个 Worker 失败时，作业明确进入了一个 `Restarting` 状态。由 Kubeflow training operator 实现的重启实际上是先删除再重建，导致的后果是 Pod 的 RESTARTS 次数每次都被清零，因此重启次数不再受限制。
