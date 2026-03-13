# Kubeflow 作业挂起的实验

Kubeflow 作业有一个 Suspended 状态。通过设置 `.spec.runPolicy.suspend` 可以使作业进入 Suspended 状态。

```console
$ yq '.spec.runPolicy.suspend = true' pytorchjob.yaml | kubectl apply -f -
pytorchjob.kubeflow.org/pytest created
```

通过修改设置 `.spec.runPolicy.suspend` 可以使已经存在的作业进入或退出 Suspended 状态：

```console
$ kubectl patch pytorchjob pytest --type=merge -p '{"spec": {"runPolicy": {"suspend": false}}}'
pytorchjob.kubeflow.org/pytest patched
```

在以下实验中，作业启动时设为 Suspended 状态，55s 时使其退出 Suspended 状态，67s 再次进入 Suspended 状态。

监视 PyTorchJob 的状态：

```console
$ kubectl get pytorchjob -owide -w
NAME     STATE   AGE
pytest           0s
pytest   Suspended   0s
pytest   Suspended   52s
pytest   Suspended   52s
pytest   Suspended   53s
pytest   Running     55s
pytest   Running     59s
pytest   Running     59s
pytest   Running     60s
pytest   Running     67s
pytest   Suspended   67s
```

监视 Pod 的状态：

```console
NAME              READY   STATUS    RESTARTS   AGE   IP       NODE     NOMINATED NODE   READINESS GATES
pytest-master-0   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
pytest-worker-0   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
pytest-worker-1   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
pytest-worker-2   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
pytest-master-0   0/1     Pending   0          1s    <none>   las1     <none>           <none>
pytest-worker-0   0/1     Pending   0          1s    <none>   las1     <none>           <none>
pytest-worker-2   0/1     Pending   0          1s    <none>   las1     <none>           <none>
pytest-worker-1   0/1     Pending   0          1s    <none>   las1     <none>           <none>
pytest-master-0   0/1     ContainerCreating   0          1s    <none>   las1     <none>           <none>
pytest-worker-1   0/1     Init:0/1            0          1s    <none>   las1     <none>           <none>
pytest-worker-0   0/1     Init:0/1            0          1s    <none>   las1     <none>           <none>
pytest-worker-2   0/1     Init:0/1            0          1s    <none>   las1     <none>           <none>
pytest-master-0   0/1     ContainerCreating   0          2s    <none>   las1     <none>           <none>
pytest-worker-0   0/1     Init:0/1            0          2s    <none>   las1     <none>           <none>
pytest-worker-2   0/1     Init:0/1            0          2s    <none>   las1     <none>           <none>
pytest-worker-1   0/1     Init:0/1            0          2s    <none>   las1     <none>           <none>
pytest-worker-0   0/1     Init:0/1            0          2s    192.168.221.183   las1     <none>           <none>
pytest-master-0   1/1     Running             0          2s    192.168.221.184   las1     <none>           <none>
pytest-worker-2   0/1     Init:0/1            0          3s    192.168.221.137   las1     <none>           <none>
pytest-worker-1   0/1     Init:0/1            0          3s    192.168.221.180   las1     <none>           <none>
pytest-worker-2   0/1     PodInitializing     0          5s    192.168.221.137   las1     <none>           <none>
pytest-worker-1   0/1     PodInitializing     0          5s    192.168.221.180   las1     <none>           <none>
pytest-worker-0   0/1     PodInitializing     0          5s    192.168.221.183   las1     <none>           <none>
pytest-worker-1   1/1     Running             0          6s    192.168.221.180   las1     <none>           <none>
pytest-worker-0   1/1     Running             0          6s    192.168.221.183   las1     <none>           <none>
pytest-worker-2   1/1     Running             0          6s    192.168.221.137   las1     <none>           <none>
pytest-master-0   1/1     Terminating         0          14s   192.168.221.184   las1     <none>           <none>
pytest-worker-0   1/1     Terminating         0          14s   192.168.221.183   las1     <none>           <none>
pytest-worker-1   1/1     Terminating         0          14s   192.168.221.180   las1     <none>           <none>
pytest-worker-2   1/1     Terminating         0          14s   192.168.221.137   las1     <none>           <none>
pytest-master-0   1/1     Terminating         0          14s   192.168.221.184   las1     <none>           <none>
pytest-worker-0   1/1     Terminating         0          14s   192.168.221.183   las1     <none>           <none>
pytest-master-0   0/1     Error               0          15s   192.168.221.184   las1     <none>           <none>
pytest-worker-1   1/1     Terminating         0          15s   192.168.221.180   las1     <none>           <none>
pytest-worker-2   1/1     Terminating         0          15s   192.168.221.137   las1     <none>           <none>
pytest-worker-0   0/1     Error               0          15s   192.168.221.183   las1     <none>           <none>
pytest-worker-1   0/1     Error               0          15s   192.168.221.180   las1     <none>           <none>
pytest-worker-2   0/1     Error               0          15s   192.168.221.137   las1     <none>           <none>
pytest-worker-0   0/1     Error               0          15s   192.168.221.183   las1     <none>           <none>
pytest-worker-0   0/1     Error               0          15s   192.168.221.183   las1     <none>           <none>
pytest-worker-2   0/1     Error               0          15s   192.168.221.137   las1     <none>           <none>
pytest-worker-2   0/1     Error               0          16s   192.168.221.137   las1     <none>           <none>
pytest-master-0   0/1     Error               0          16s   192.168.221.184   las1     <none>           <none>
pytest-master-0   0/1     Error               0          16s   192.168.221.184   las1     <none>           <none>
pytest-worker-1   0/1     Error               0          16s   192.168.221.180   las1     <none>           <none>
pytest-worker-1   0/1     Error               0          16s   192.168.221.180   las1     <none>           <none>
```

可见使作业进入 Suspended 状态等价于删除所有正在运行的 Pod.
