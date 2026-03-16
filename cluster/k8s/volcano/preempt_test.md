# Volcano 作业抢占式调度实验

本文适用于 Volcano `1.12.1`.

## 准备工作

Volcano 作业使用 PriorityClass 定义优先级。首先定义一个 PriorityClass:

:::{literalinclude} /_files/macos/workspace/k8s/high_pc.yaml
:::

其名称为 `high-priority`, value 为 10000, 高于默认优先级的 0. 将以上文本保存为文件 `high_pc.yaml` 然后应用到 k8s 集群：

```console
$ kubectl apply -f high_pc.yaml 
priorityclass.scheduling.k8s.io/high-priority created
```

## 在默认配置下

Volcano 调度器可以通过配置控制其行为，查看配置：

:::{literalinclude} /_files/macos/console/kubectl/get_cm_volcano_scheduler.txt
:language: console
:::

以上为 `1.12.1` 安装后的默认配置。

### 实验一、队列中可以按优先级排序

定义一个 Volcano 队列用于测试：

:::{literalinclude} /_files/macos/workspace/k8s/volcano/test_q_1c.yaml
:::

其名称为 `test`, 容量为 1 个 CPU. 将以上文本保存为文件 `test_q_1c.yaml` 然后应用到 k8s 集群：

```console
$ kubectl apply -f test_q_1c.yaml
queue.scheduling.volcano.sh/test created
```

定义一个 Volcano 作业:

:::{literalinclude} /_files/macos/workspace/k8s/volcano/sleep_vj_normal.yaml
:::

其名称为 `sleep-normal`. 此作业包含 3 个任务，每个任务需要的资源为 1 个 CPU. 任务的内容是等待 1 分钟后退出。

将上述文本保存为文件 `sleep_vj_normal.yaml`. 同时另存为文件 `sleep_vj_high.yaml` 并作如下修改：

:::{literalinclude} /_files/macos/workspace/k8s/volcano/sleep_vj_high.yaml
:diff: /_files/macos/workspace/k8s/volcano/sleep_vj_normal.yaml
:::

将名称改为了 `sleep-high` 并使用了高优先级。

:::{note}
高优先级的定义 `priorityClassName: high-priority` 必须在 `Job` 和 `Pod` 两个层级同时出现，这一点对后面的运行时抢占十分重要。
:::

先后提交作业 `sleep-normal` 和 `sleep-high`:

```console
$ kubectl create -f sleep_vj_normal.yaml
job.batch.volcano.sh/sleep-normal created
$ kubectl create -f sleep_vj_high.yaml 
job.batch.volcano.sh/sleep-high created
```

由于队列 `test` 的 CPU 个数不够，两个作业都处于 Pending 状态：

```console
$ kubectl get vj -owide
NAME           STATUS    MINAVAILABLE   RUNNINGS   AGE   QUEUE
sleep-high     Pending   3                         8s    test
sleep-normal   Pending   3                         19s   test
```

如果装了 `vcctl` 工具，可以看到更详细的信息：

```console
$ vcctl job list
Name           Creation       Phase       JobType     Replicas    Min   Pending   Running   Succeeded   Failed    Unknown     RetryCount
sleep-high     2025-07-14     Pending     Batch       3           3     0         0         0           0         0           0
sleep-normal   2025-07-14     Pending     Batch       3           3     0         0         0           0         0           0
$ vcctl queue get --name test
Name                     Weight  State   Inqueue Pending Running Unknown Completed
test                     1       Open    0       2       0       0       0
```

修改队列 `test` 的定义：

```console
$ kubectl edit q test
queue.scheduling.volcano.sh/test edited
```

修改内容为增加 CPU 个数，如下：

:::{literalinclude} /_files/macos/workspace/k8s/volcano/test_q_4c.yaml
:diff: /_files/macos/workspace/k8s/volcano/test_q_1c.yaml
:::

由于资源数量增加，有作业开始运行：

```console
$ kubectl get vj -owide
NAME           STATUS    MINAVAILABLE   RUNNINGS   AGE     QUEUE
sleep-high     Running   3              3          2m23s   test
sleep-normal   Pending   3                         2m34s   test
$ vcctl job list
Name           Creation       Phase       JobType     Replicas    Min   Pending   Running   Succeeded   Failed    Unknown     RetryCount
sleep-high     2025-07-14     Running     Batch       3           3     0         3         0           0         0           0
sleep-normal   2025-07-14     Pending     Batch       3           3     0         0         0           0         0           0
$ vcctl queue get --name test
Name                     Weight  State   Inqueue Pending Running Unknown Completed
test                     1       Open    0       1       1       0       0
```

可以看到优先级较高的作业首先得到运行。

### 实验二、运行中的作业不能被抢占

如前述设置，队列中的 CPU 个数设置为 4. 先提交默认优先级的任务 `sleep-normal`, 候其运行后再提交高优先级任务 `sleep-high`:

```console
$ kubectl create -f sleep_vj_normal.yaml 
job.batch.volcano.sh/sleep-normal created
$ kubectl get vj sleep-normal
NAME           STATUS    MINAVAILABLE   RUNNINGS   AGE
sleep-normal   Running   3              3          10s
$ kubectl create -f sleep_vj_high.yaml 
job.batch.volcano.sh/sleep-high created
```

检查作业状态：

```console
$ kubectl get vj
NAME           STATUS    MINAVAILABLE   RUNNINGS   AGE
sleep-high     Pending   3                         3s
sleep-normal   Running   3              3          22s
$ vcctl job list
Name           Creation       Phase       JobType     Replicas    Min   Pending   Running   Succeeded   Failed    Unknown     RetryCount
sleep-high     2025-07-14     Pending     Batch       3           3     0         0         0           0         0           0
sleep-normal   2025-07-14     Running     Batch       3           3     0         3         0           0         0           0
$ vcctl queue get --name test
Name                     Weight  State   Inqueue Pending Running Unknown Completed
test                     1       Open    0       1       1       0       0
```

可以看出低优先级任务仍处于 Running 状态，高优先级作业处于 Pending 状态。

## 启用运行时抢占

对 Volcano 调度器的配置进行修改：

```console
$ kubectl edit cm volcano-scheduler-configmap -n volcano-system
configmap/volcano-scheduler-configmap edited
```

修改内容如下：

:::{literalinclude} /_files/macos/console/kubectl/get_cm_volcano_scheduler_preempt.txt
:diff: /_files/macos/console/kubectl/get_cm_volcano_scheduler.txt
:::

:::{note}
这里特别要注意把 `overcommit` 插件挪到 `gang` 的前面。
:::

### 实验三、高优先作业抢占运行中的低优先级作业

为了观察作业的状态变化，在另一个终端中监视作业状态：

```console
$ kubectl get vj -owide -w
```

队列和作业设置同实验二，先提交默认优先级的作业 `sleep-normal`, 候其运行后再提交高优先级作业 `sleep-high`:

```console
$ kubectl create -f sleep_vj_normal.yaml 
job.batch.volcano.sh/sleep-normal created
$ kubectl create -f sleep_vj_high.yaml 
job.batch.volcano.sh/sleep-high created
```

在另一个终端中的输出：

```console
NAME           STATUS   MINAVAILABLE   RUNNINGS   AGE   QUEUE
sleep-normal                                      0s    test
sleep-normal   Pending   3                         0s    test
sleep-normal   Pending   3                         1s    test
sleep-normal   Pending   3              1          3s    test
sleep-normal   Pending   3              2          4s    test
sleep-normal   Running   3              3          4s    test
sleep-high                                         0s    test
sleep-high     Pending   3                         0s    test
sleep-high     Pending   3                         1s    test
sleep-normal   Restarting   3                         19s   test
sleep-normal   Pending      3                         19s   test
sleep-normal   Pending      3                         20s   test
sleep-normal   Pending      3                         20s   test
sleep-high     Pending      3              1          5s    test
sleep-high     Pending      3              2          5s    test
sleep-high     Running      3              3          5s    test
sleep-high     Running      3              2          65s   test
sleep-high     Running      3              1          66s   test
sleep-high     Completing   3                         66s   test
sleep-high     Completed    3                         66s   test
sleep-high     Completed    3                         66s   test
sleep-normal   Pending      3              1          85s   test
sleep-normal   Pending      3              2          85s   test
sleep-normal   Running      3              3          85s   test
sleep-normal   Running      3              2          2m26s   test
sleep-normal   Running      3              1          2m27s   test
sleep-normal   Completing   3                         2m27s   test
sleep-normal   Completed    3                         2m27s   test
sleep-normal   Completed    3                         2m27s   test
```

可以看到，高优先级作业提交后，低优先级作业被重置，然后进入 `Pending` 状态，高优先级作业得到运行。另外可以看到，作业的 3 个任务实例总是同时被调度，符合 `GANG` 调度的特征。
