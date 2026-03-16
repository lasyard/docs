# Volcano 分层队列实验

修改 Volcano 调度器配置，使能 `capacity` 插件：

```console
$ kubectl edit cm -n volcano-system volcano-scheduler-configmap
configmap/volcano-scheduler-configmap edited
```

修改内容如下：

:::{literalinclude} /_files/macos/console/kubectl/get_cm_volcano_scheduler_capacity.txt
:diff: /_files/macos/console/kubectl/get_cm_volcano_scheduler.txt
:::

:::{note}
`capacity` 插件和 `proportion` 插件互斥，不能同时使用。
:::

编辑文件 `hierarchical_q.yaml`, 内容如下：

:::{literalinclude} /_files/macos/workspace/k8s/volcano/hierarchical_q.yaml
:::

应用到集群：

```console
$ kubectl apply -f hierarchical_q.yaml 
queue.scheduling.volcano.sh/a created
queue.scheduling.volcano.sh/a1 created
queue.scheduling.volcano.sh/a2 created
```

查看队列：

```console
$ kubectl get q
NAME      PARENT
a         root
a1        a
a2        a
default   root
root
```

## 实险一：队列资源限制和借用

创建一个 vcjob, 配置如下：

:::{literalinclude} /_files/macos/workspace/k8s/volcano/hierarchical_vj_a1.yaml
:::

这个作业将提交到队列 `a1`. 提交到集群之后，观察其状态：

```console
$ kubectl get vj -owide -w
NAME   STATUS   MINAVAILABLE   RUNNINGS   AGE   QUEUE
a1                                        0s    a1
a1     Pending   1                         0s    a1
a1     Pending   1                         0s    a1
a1     Running   1              1          2s    a1
a1     Running   1              2          3s    a1
a1     Running   1              3          3s    a1
a1     Running   1              4          3s    a1
a1     Running   1              3          64s   a1
a1     Running   1              2          64s   a1
a1     Running   1              1          64s   a1
a1     Running   1                         65s   a1
a1     Running   1              1          65s   a1
a1     Running   1              2          65s   a1
a1     Running   1              3          66s   a1
a1     Running   1              4          66s   a1
a1     Running   1              3          2m7s   a1
a1     Running   1              2          2m7s   a1
a1     Running   1              1          2m7s   a1
a1     Completing   1                         2m8s   a1
a1     Completed    1                         2m8s   a1
a1     Completed    1                         2m8s   a1
```

可见虽然队列 `a1` 没有限制 `capability`, 但是作业受其父队列 `a` 的限制，CPU 个数不能超过 4. 但由于作业设置的最小任务数为 1, 只需要 1 个 CPU 即可满足，所以被调度，并且利用了全部可用的资源。此时队列 `a2` 的资源实际上被“借用”了。

监视 Pod 的状态可以看到更多的细节：

```console
$ kubectl get po -owide -w
NAME              READY   STATUS    RESTARTS   AGE   IP       NODE     NOMINATED NODE   READINESS GATES
a1-sleep-task-7   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
a1-sleep-task-2   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
a1-sleep-task-0   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
a1-sleep-task-4   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
a1-sleep-task-6   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
a1-sleep-task-5   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
a1-sleep-task-3   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
a1-sleep-task-1   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
a1-sleep-task-1   0/1     Pending   0          1s    <none>   las1     <none>           <none>
a1-sleep-task-2   0/1     Pending   0          1s    <none>   las1     <none>           <none>
a1-sleep-task-3   0/1     Pending   0          1s    <none>   las1     <none>           <none>
a1-sleep-task-0   0/1     Pending   0          1s    <none>   las1     <none>           <none>
a1-sleep-task-4   0/1     Pending   0          1s    <none>   <none>   <none>           <none>
a1-sleep-task-7   0/1     Pending   0          1s    <none>   <none>   <none>           <none>
a1-sleep-task-6   0/1     Pending   0          1s    <none>   <none>   <none>           <none>
a1-sleep-task-5   0/1     Pending   0          1s    <none>   <none>   <none>           <none>
a1-sleep-task-1   0/1     ContainerCreating   0          1s    <none>   las1     <none>           <none>
a1-sleep-task-2   0/1     ContainerCreating   0          1s    <none>   las1     <none>           <none>
a1-sleep-task-0   0/1     ContainerCreating   0          1s    <none>   las1     <none>           <none>
a1-sleep-task-3   0/1     ContainerCreating   0          1s    <none>   las1     <none>           <none>
a1-sleep-task-3   0/1     ContainerCreating   0          2s    <none>   las1     <none>           <none>
a1-sleep-task-2   0/1     ContainerCreating   0          2s    <none>   las1     <none>           <none>
a1-sleep-task-1   0/1     ContainerCreating   0          2s    <none>   las1     <none>           <none>
a1-sleep-task-0   0/1     ContainerCreating   0          2s    <none>   las1     <none>           <none>
a1-sleep-task-3   1/1     Running             0          2s    192.168.221.181   las1     <none>           <none>
a1-sleep-task-5   0/1     Pending             0          2s    <none>            <none>   <none>           <none>
a1-sleep-task-6   0/1     Pending             0          2s    <none>            <none>   <none>           <none>
a1-sleep-task-4   0/1     Pending             0          2s    <none>            <none>   <none>           <none>
a1-sleep-task-7   0/1     Pending             0          2s    <none>            <none>   <none>           <none>
a1-sleep-task-0   1/1     Running             0          3s    192.168.221.187   las1     <none>           <none>
a1-sleep-task-1   1/1     Running             0          3s    192.168.221.185   las1     <none>           <none>
a1-sleep-task-2   1/1     Running             0          3s    192.168.221.191   las1     <none>           <none>
a1-sleep-task-4   0/1     Pending             0          3s    <none>            <none>   <none>           <none>
a1-sleep-task-7   0/1     Pending             0          3s    <none>            <none>   <none>           <none>
a1-sleep-task-5   0/1     Pending             0          3s    <none>            <none>   <none>           <none>
a1-sleep-task-6   0/1     Pending             0          3s    <none>            <none>   <none>           <none>
a1-sleep-task-1   0/1     Completed           0          62s   192.168.221.185   las1     <none>           <none>
a1-sleep-task-3   0/1     Completed           0          62s   192.168.221.181   las1     <none>           <none>
a1-sleep-task-2   0/1     Completed           0          62s   192.168.221.191   las1     <none>           <none>
a1-sleep-task-0   0/1     Completed           0          63s   192.168.221.187   las1     <none>           <none>
...
```

这里可以观察到：

- 虽然资源只允许 4 个任务被调度，但实际上所有任务对应的 Pod 从一开始就都被创建出来了
- 被调度的 4 个任务分配在一个节点上

## 实验二：资源回收

再创建另一个 vcjob, 配置与之前相同，只是将队列改为 `a2`:

:::{literalinclude} /_files/macos/workspace/k8s/volcano/hierarchical_vj_a2.yaml
:diff: /_files/macos/workspace/k8s/volcano/hierarchical_vj_a1.yaml
:::

删除刚才的作业 `a1`. 然后重新提交 `a1`, 候其 4 个任务运行后提交 `a2`, 观察作业状态变化：

```console
$ kubectl get vj -owide -w
NAME   STATUS   MINAVAILABLE   RUNNINGS   AGE   QUEUE
a1                                        0s    a1
a1     Pending   1                         0s    a1
a1     Pending   1                         1s    a1
a1     Running   1              1          4s    a1
a1     Running   1              2          4s    a1
a1     Running   1              3          4s    a1
a1     Running   1              4          4s    a1
a2                                         0s    a2
a2     Pending   1                         0s    a2
a2     Pending   1                         1s    a2
a1     Restarting   1                         15s   a1
a1     Pending      1                         15s   a1
a1     Pending      1                         17s   a1
a1     Pending      1                         17s   a1
a1     Pending      1                         17s   a1
a1     Pending      1                         17s   a1
a2     Running      1              1          5s    a2
a1     Running      1              1          18s   a1
a2     Running      1              2          5s    a2
a1     Running      1              2          18s   a1
a2     Running      1              1          66s   a2
a2     Running      1                         66s   a2
a1     Running      1              1          79s   a1
a1     Running      1                         79s   a1
a1     Running      1              1          81s   a1
a2     Running      1              1          68s   a2
a1     Running      1              2          81s   a1
a2     Running      1              2          68s   a2
a1     Running      1              1          2m22s   a1
a1     Running      1                         2m23s   a1
a2     Running      1              1          2m10s   a2
a2     Running      1                         2m10s   a2
a2     Running      1              1          2m11s   a2
a1     Running      1              1          2m24s   a1
a1     Running      1              2          2m24s   a1
a2     Running      1              2          2m12s   a2
a2     Running      1              1          3m13s   a2
a1     Running      1              1          3m26s   a1
a2     Running      1                         3m13s   a2
a1     Running      1                         3m26s   a1
a2     Running      1              1          3m14s   a2
a2     Running      1              2          3m14s   a2
a1     Running      1              1          3m28s   a1
a1     Running      1              2          3m28s   a1
a1     Running      1              1          4m29s   a1
a1     Completing   1                         4m29s   a1
a1     Completed    1                         4m29s   a1
a1     Completed    1                         4m29s   a1
a2     Running      1              1          4m16s   a2
a2     Completing   1                         4m16s   a2
a2     Completed    1                         4m16s   a2
a2     Completed    1                         4m16s   a2
```

可以看到，当作业 `a2` 提交时，作业 `a1` 借用的资源需要收回，因此被重启。两个作业以各自队列 `deserved` 资源同时运行。观察 Pod 的状态变化可更清楚地发现：作业重启是将所有的 Pod 全部终结再重新入队：

```console
$ kubectl get po -owide -w
NAME              READY   STATUS    RESTARTS   AGE   IP       NODE     NOMINATED NODE   READINESS GATES
...
a1-sleep-task-3   1/1     Running             0          3s    192.168.221.176   las1     <none>           <none>
a1-sleep-task-1   1/1     Running             0          3s    192.168.221.138   las1     <none>           <none>
a1-sleep-task-0   1/1     Running             0          3s    192.168.221.135   las1     <none>           <none>
a1-sleep-task-2   1/1     Running             0          3s    192.168.221.141   las1     <none>           <none>
a1-sleep-task-6   0/1     Pending             0          3s    <none>            <none>   <none>           <none>
a1-sleep-task-4   0/1     Pending             0          3s    <none>            <none>   <none>           <none>
a1-sleep-task-5   0/1     Pending             0          3s    <none>            <none>   <none>           <none>
a1-sleep-task-7   0/1     Pending             0          3s    <none>            <none>   <none>           <none>
a2-sleep-task-6   0/1     Pending             0          0s    <none>            <none>   <none>           <none>
a2-sleep-task-1   0/1     Pending             0          0s    <none>            <none>   <none>           <none>
a2-sleep-task-5   0/1     Pending             0          0s    <none>            <none>   <none>           <none>
a2-sleep-task-3   0/1     Pending             0          0s    <none>            <none>   <none>           <none>
a2-sleep-task-2   0/1     Pending             0          0s    <none>            <none>   <none>           <none>
a2-sleep-task-7   0/1     Pending             0          0s    <none>            <none>   <none>           <none>
a2-sleep-task-0   0/1     Pending             0          0s    <none>            <none>   <none>           <none>
a2-sleep-task-4   0/1     Pending             0          0s    <none>            <none>   <none>           <none>
a1-sleep-task-3   1/1     Running             0          14s   192.168.221.176   las1     <none>           <none>
a1-sleep-task-3   1/1     Terminating         0          14s   192.168.221.176   las1     <none>           <none>
a1-sleep-task-5   0/1     Pending             0          14s   <none>            <none>   <none>           <none>
a1-sleep-task-7   0/1     Pending             0          14s   <none>            <none>   <none>           <none>
a1-sleep-task-4   0/1     Pending             0          14s   <none>            <none>   <none>           <none>
a2-sleep-task-6   0/1     Pending             0          1s    <none>            <none>   <none>           <none>
a2-sleep-task-2   0/1     Pending             0          1s    <none>            <none>   <none>           <none>
a1-sleep-task-6   0/1     Pending             0          14s   <none>            <none>   <none>           <none>
a2-sleep-task-5   0/1     Pending             0          1s    <none>            <none>   <none>           <none>
a2-sleep-task-1   0/1     Pending             0          1s    <none>            <none>   <none>           <none>
a2-sleep-task-3   0/1     Pending             0          1s    <none>            <none>   <none>           <none>
a2-sleep-task-4   0/1     Pending             0          1s    <none>            <none>   <none>           <none>
a2-sleep-task-7   0/1     Pending             0          1s    <none>            <none>   <none>           <none>
a1-sleep-task-1   1/1     Terminating         0          14s   192.168.221.138   las1     <none>           <none>
a2-sleep-task-0   0/1     Pending             0          1s    <none>            <none>   <none>           <none>
a1-sleep-task-3   1/1     Terminating         0          14s   192.168.221.176   las1     <none>           <none>
a1-sleep-task-2   1/1     Terminating         0          14s   192.168.221.141   las1     <none>           <none>
a1-sleep-task-7   0/1     Terminating         0          14s   <none>            <none>   <none>           <none>
a1-sleep-task-7   0/1     Terminating         0          14s   <none>            <none>   <none>           <none>
a1-sleep-task-5   0/1     Terminating         0          14s   <none>            <none>   <none>           <none>
a1-sleep-task-5   0/1     Terminating         0          14s   <none>            <none>   <none>           <none>
a1-sleep-task-0   1/1     Terminating         0          14s   192.168.221.135   las1     <none>           <none>
a1-sleep-task-6   0/1     Terminating         0          14s   <none>            <none>   <none>           <none>
a1-sleep-task-6   0/1     Terminating         0          14s   <none>            <none>   <none>           <none>
a1-sleep-task-4   0/1     Terminating         0          14s   <none>            <none>   <none>           <none>
a1-sleep-task-4   0/1     Terminating         0          14s   <none>            <none>   <none>           <none>
a1-sleep-task-7   0/1     Pending             0          0s    <none>            <none>   <none>           <none>
a1-sleep-task-5   0/1     Pending             0          0s    <none>            <none>   <none>           <none>
a1-sleep-task-6   0/1     Pending             0          0s    <none>            <none>   <none>           <none>
a1-sleep-task-4   0/1     Pending             0          0s    <none>            <none>   <none>           <none>
a1-sleep-task-3   1/1     Terminating         0          15s   192.168.221.176   las1     <none>           <none>
a1-sleep-task-2   1/1     Terminating         0          15s   192.168.221.141   las1     <none>           <none>
a1-sleep-task-1   1/1     Terminating         0          15s   192.168.221.138   las1     <none>           <none>
a1-sleep-task-0   1/1     Terminating         0          15s   192.168.221.135   las1     <none>           <none>
a1-sleep-task-3   0/1     Error               0          15s   192.168.221.176   las1     <none>           <none>
a1-sleep-task-1   0/1     Error               0          15s   192.168.221.138   las1     <none>           <none>
a1-sleep-task-2   0/1     Error               0          15s   192.168.221.141   las1     <none>           <none>
a1-sleep-task-0   0/1     Error               0          15s   192.168.221.135   las1     <none>           <none>
a1-sleep-task-7   0/1     Pending             0          1s    <none>            <none>   <none>           <none>
a1-sleep-task-6   0/1     Pending             0          1s    <none>            <none>   <none>           <none>
a2-sleep-task-7   0/1     Pending             0          2s    <none>            <none>   <none>           <none>
a2-sleep-task-6   0/1     Pending             0          2s    <none>            <none>   <none>           <none>
a2-sleep-task-5   0/1     Pending             0          2s    <none>            <none>   <none>           <none>
a2-sleep-task-4   0/1     Pending             0          2s    <none>            <none>   <none>           <none>
a2-sleep-task-3   0/1     Pending             0          2s    <none>            <none>   <none>           <none>
a2-sleep-task-2   0/1     Pending             0          2s    <none>            <none>   <none>           <none>
a2-sleep-task-1   0/1     Pending             0          2s    <none>            las1     <none>           <none>
a1-sleep-task-4   0/1     Pending             0          1s    <none>            las1     <none>           <none>
a1-sleep-task-5   0/1     Pending             0          1s    <none>            las1     <none>           <none>
a2-sleep-task-0   0/1     Pending             0          2s    <none>            las1     <none>           <none>
a2-sleep-task-1   0/1     ContainerCreating   0          2s    <none>            las1     <none>           <none>
a1-sleep-task-4   0/1     ContainerCreating   0          1s    <none>            las1     <none>           <none>
a2-sleep-task-0   0/1     ContainerCreating   0          2s    <none>            las1     <none>           <none>
a1-sleep-task-5   0/1     ContainerCreating   0          1s    <none>            las1     <none>           <none>
a1-sleep-task-1   0/1     Error               0          16s   192.168.221.138   las1     <none>           <none>
a1-sleep-task-1   0/1     Error               0          16s   192.168.221.138   las1     <none>           <none>
a1-sleep-task-1   0/1     Pending             0          0s    <none>            <none>   <none>           <none>
a1-sleep-task-0   0/1     Error               0          16s   192.168.221.135   las1     <none>           <none>
a1-sleep-task-0   0/1     Error               0          16s   192.168.221.135   las1     <none>           <none>
a1-sleep-task-0   0/1     Pending             0          0s    <none>            <none>   <none>           <none>
a1-sleep-task-2   0/1     Error               0          16s   192.168.221.141   las1     <none>           <none>
a1-sleep-task-2   0/1     Error               0          16s   192.168.221.141   las1     <none>           <none>
a1-sleep-task-2   0/1     Pending             0          0s    <none>            <none>   <none>           <none>
a1-sleep-task-3   0/1     Error               0          16s   192.168.221.176   las1     <none>           <none>
a1-sleep-task-3   0/1     Error               0          16s   192.168.221.176   las1     <none>           <none>
a1-sleep-task-3   0/1     Pending             0          0s    <none>            <none>   <none>           <none>
a2-sleep-task-1   0/1     ContainerCreating   0          3s    <none>            las1     <none>           <none>
a1-sleep-task-4   0/1     ContainerCreating   0          2s    <none>            las1     <none>           <none>
a1-sleep-task-5   0/1     ContainerCreating   0          2s    <none>            las1     <none>           <none>
a2-sleep-task-0   0/1     ContainerCreating   0          3s    <none>            las1     <none>           <none>
a2-sleep-task-2   0/1     Pending             0          3s    <none>            <none>   <none>           <none>
a2-sleep-task-5   0/1     Pending             0          3s    <none>            <none>   <none>           <none>
a2-sleep-task-3   0/1     Pending             0          3s    <none>            <none>   <none>           <none>
a2-sleep-task-7   0/1     Pending             0          3s    <none>            <none>   <none>           <none>
a2-sleep-task-4   0/1     Pending             0          3s    <none>            <none>   <none>           <none>
a2-sleep-task-6   0/1     Pending             0          3s    <none>            <none>   <none>           <none>
a1-sleep-task-3   0/1     Pending             0          0s    <none>            <none>   <none>           <none>
a1-sleep-task-2   0/1     Pending             0          0s    <none>            <none>   <none>           <none>
a1-sleep-task-6   0/1     Pending             0          2s    <none>            <none>   <none>           <none>
a1-sleep-task-1   0/1     Pending             0          0s    <none>            <none>   <none>           <none>
a1-sleep-task-7   0/1     Pending             0          2s    <none>            <none>   <none>           <none>
a1-sleep-task-0   0/1     Pending             0          0s    <none>            <none>   <none>           <none>
a2-sleep-task-1   1/1     Running             0          4s    192.168.221.160   las1     <none>           <none>
a1-sleep-task-4   1/1     Running             0          3s    192.168.221.184   las1     <none>           <none>
a2-sleep-task-0   1/1     Running             0          4s    192.168.221.146   las1     <none>           <none>
a1-sleep-task-5   1/1     Running             0          3s    192.168.221.140   las1     <none>           <none>
...
```

## 实验三：资源独占

同实验一，修改队列 `a2` 的 `deserved` 资源为 `guarantee`:

```console
$ kubectl edit q a2
queue.scheduling.volcano.sh/a2 edited
```

修改内容如下：

:::{literalinclude} /_files/macos/console/kubectl/get_q_a2_guarantee.txt
:diff: /_files/macos/console/kubectl/get_q_a2.txt
:::

提交作业 `a1`, 观察其状态变化：

```console
$ kubectl get vj -owide -w
NAME   STATUS   MINAVAILABLE   RUNNINGS   AGE   QUEUE
a1                                        0s    a1
a1     Pending   1                         0s    a1
a1     Pending   1                         0s    a1
a1     Running   1              1          2s    a1
a1     Running   1              2          2s    a1
a1     Running   1              1          64s   a1
a1     Running   1                         64s   a1
a1     Running   1              1          65s   a1
a1     Running   1              2          66s   a1
a1     Running   1              1          2m7s   a1
a1     Running   1                         2m7s   a1
a1     Running   1              1          2m9s   a1
a1     Running   1              2          2m10s   a1
a1     Running   1              1          3m10s   a1
a1     Running   1                         3m10s   a1
a1     Running   1              1          3m13s   a1
a1     Running   1              2          3m13s   a1
a1     Running   1              1          4m13s   a1
a1     Completing   1                         4m14s   a1
a1     Completed    1                         4m14s   a1
a1     Completed    1                         4m14s   a1
```

可以看出，作业 `a1` 不再能借用队列 `a2` 的资源了，相当于队列 `a2` 的资源被独占了。
