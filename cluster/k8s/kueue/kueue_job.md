# Kueue 作业实验

## 准备工作

首先建立一个 LocalQueue 用于作业排队：

:::{literalinclude} /_files/macos/workspace/k8s/kueue/test_lq.yaml
:::

Kueue 的作业队列结构比较复杂，包含以下资源：

- ResourceFlavor: 通过节点标签可以限制可调度的节点范围，通过 `toleration` 设置可以容忍污点
- ClusterQueue: 全局作业队列，定义了队列的容量和 ResourceFlavor
- LocalQueue: 命名空间局域的队列，映射到一个全局作业队列，是作业提交时实际使用的队列

将以上文本保存为文件 `test_lq.yaml`, 应用到集群：

```console
$ kubectl apply -f test_lq.yaml
resourceflavor.kueue.x-k8s.io/default created
clusterqueue.kueue.x-k8s.io/test created
localqueue.kueue.x-k8s.io/test created
$ kubectl get rf,cq,lq -owide
NAME                                    AGE
resourceflavor.kueue.x-k8s.io/default   24s

NAME                               COHORT   STRATEGY         PENDING WORKLOADS   ADMITTED WORKLOADS
clusterqueue.kueue.x-k8s.io/test            BestEffortFIFO   0                   0

NAME                             CLUSTERQUEUE   PENDING WORKLOADS   ADMITTED WORKLOADS
localqueue.kueue.x-k8s.io/test   test           0                   0
```

## 实验一、无队列的作业调度

定义一个 `batch/v1` 版本的作业：

:::{literalinclude} /_files/macos/workspace/k8s/kueue/sleep_job.yaml
:::

其中规定了并行度为 3, 并且需要 3 个 Pod 完成后 Job 才算完成，而每个 Pod 需要 1 个 CPU. 假设系统中仅有一个 CPU, 那么提交上述作业后：

```console
$ kubectl get job,po
NAME                     STATUS    COMPLETIONS   DURATION   AGE
job.batch/sleep-normal   Running   0/3           15s        15s

NAME                       READY   STATUS    RESTARTS   AGE
pod/sleep-normal-0-67psd   1/1     Running   0          15s
pod/sleep-normal-1-jq8rr   0/1     Pending   0          15s
pod/sleep-normal-2-pmm58   0/1     Pending   0          15s
```

可见系统并不保证 3 个 Pod 同时运行，这在很多并行计算的情况是不可接受的。

## 实验二、使用 Kueue 队列的作业调度

修改实验一中的作业定义：

:::{literalinclude} /_files/macos/workspace/k8s/kueue/sleep_job_kueue.yaml
:diff: /_files/macos/workspace/k8s/kueue/sleep_job.yaml
:::

增加的标签可以使 Kueue 的调度生效，使用的队列为 `test`. 提交上述作业后：

```console
NAME                                             QUEUE   RESERVED IN   ADMITTED   FINISHED   AGE
workload.kueue.x-k8s.io/job-sleep-normal-b1ce9   test    test          True                  21s

NAME                     STATUS    COMPLETIONS   DURATION   AGE
job.batch/sleep-normal   Running   0/3           21s        21s

NAME                       READY   STATUS    RESTARTS   AGE
pod/sleep-normal-0-tzkmt   0/1     Pending   0          21s
pod/sleep-normal-1-bfjt2   0/1     Pending   0          21s
pod/sleep-normal-2-2k8d8   0/1     Pending   0          21s

NAME                             CLUSTERQUEUE   PENDING WORKLOADS   ADMITTED WORKLOADS
localqueue.kueue.x-k8s.io/test   test           0                   1
```

可以发现 Kueue 将作业映射为一个 Workload 资源进行管理。因为队列的资源足够，所以作业开始运行，创建了相应的 Pod 并提交调度，但实际并没有调度起来。这是因为 ResourceFlavor 中的节点标签被写在了 Pod 的 nodeSelector 中：

```console
$ kubectl get po -o custom-columns='NAME:.metadata.name,NODE-GROUP:.spec.nodeSelector.node-group'
NAME                   NODE-GROUP
sleep-normal-0-tzkmt   default
sleep-normal-1-bfjt2   default
sleep-normal-2-2k8d8   default
```

:::{tip}
Kueue 0.16.2 中 ResourceFlavor 定义已支持不设 nodeLabels.
:::

查看其中一个 Pod 的事件：

```console
$ kubectl get event --field-selector involvedObject.name=sleep-normal-0-tzkmt
LAST SEEN   TYPE      REASON             OBJECT                     MESSAGE
18m         Warning   FailedScheduling   pod/sleep-normal-0-tzkmt   0/4 nodes are available: 1 node(s) had untolerated taint {node-role.kubernetes.io/control-plane: }, 3 node(s) didn't match Pod's node affinity/selector. no new claims to deallocate, preemption: 0/4 nodes are available: 4 Preemption is not helpful for scheduling.
```

可见确实是因为节点选择器不满足。对节点打标签：

```console
$ kubectl label node --all node-group=default
node/las0 labeled
node/las1 labeled
node/las2 labeled
node/las3 labeled
```

然后再查看状态：

```console
$ kubectl get wl,job,po
NAME                                             QUEUE   RESERVED IN   ADMITTED   FINISHED   AGE
workload.kueue.x-k8s.io/job-sleep-normal-b1ce9   test    test          True                  16h

NAME                     STATUS    COMPLETIONS   DURATION   AGE
job.batch/sleep-normal   Running   0/3           16h        16h

NAME                       READY   STATUS    RESTARTS   AGE
pod/sleep-normal-0-tzkmt   1/1     Running   0          16h
pod/sleep-normal-1-bfjt2   1/1     Running   0          16h
pod/sleep-normal-2-2k8d8   1/1     Running   0          16h
```

可见 Pod 都开始运行了。

## 实验二、排队优先级

因为 Job 的 `spec` 并不支持 `priorityClassName` 属性，所以 Kueue 推出一个 `WorkloadPriorityClass` 用来设置 Job 的优先级：

:::{literalinclude} /_files/macos/workspace/k8s/kueue/high_workloadpriorityclass.yaml
:::

将上述文本保存为文件 `high_workloadpriorityclass.yaml` 并应用：

```console
$ kubectl apply -f high_workloadpriorityclass.yaml
workloadpriorityclass.kueue.x-k8s.io/high-priority created
```

修改实验二中的作业定义：

:::{literalinclude} /_files/macos/workspace/k8s/kueue/sleep_job_kueue_high.yaml
:diff: /_files/macos/workspace/k8s/kueue/sleep_job_kueue.yaml
:::

为了阻止作业运行，将 ClusterQueue 的 cpu 配额降低：

```console
$ kubectl edit cq test
```

修改内容如下：

:::{literalinclude} /_files/macos/console/kubectl/get_cq_cpu_2.txt
:diff: /_files/macos/console/kubectl/get_cq_cpu_4.txt
:::

然后先提交作业 sleep-normal, 再提交作业 sleep-high. 查看状态：

```console
$ kubectl get wl,job,po
NAME                                             QUEUE   RESERVED IN   ADMITTED   FINISHED   AGE
workload.kueue.x-k8s.io/job-sleep-high-8de71     test                                        60s
workload.kueue.x-k8s.io/job-sleep-normal-1b4d8   test                                        69s

NAME                     STATUS      COMPLETIONS   DURATION   AGE
job.batch/sleep-high     Suspended   0/3                      60s
job.batch/sleep-normal   Suspended   0/3                      69s
```

可见由于队列容量不够，作业都处于 Suspended 状态，没有创建 Pod. 事实上 Workload 是作为整体准入的，有 GANG 调度的特点，但 Kueue 不是调度器。

查看队列的状态也可以发现有作业在排队：

```console
$ kubectl get lq,cq
NAME                             CLUSTERQUEUE   PENDING WORKLOADS   ADMITTED WORKLOADS
localqueue.kueue.x-k8s.io/test   test           2                   0

NAME                               COHORT   PENDING WORKLOADS
clusterqueue.kueue.x-k8s.io/test            2
```

更进一步，通过 `kubectl` 的 `kueue` 插件可以列出作业在队列中的位置：

```console
$ kubectl kueue list wl
NAME                     JOB TYPE   JOB NAME       LOCALQUEUE   CLUSTERQUEUE   STATUS    POSITION IN QUEUE   EXEC TIME   AGE
job-sleep-high-8de71     job        sleep-high     test         test           PENDING   0                               5h10m
job-sleep-normal-1b4d8   job        sleep-normal   test         test           PENDING   1                               5h10m
```

可以发现优先级高的作业排在了前面。现在修改队列的 cpu 为 4, 让其中一个作业运行起来。然后查看状态：

```console
$ kubectl get wl,job,po
NAME                                             QUEUE   RESERVED IN   ADMITTED   FINISHED   AGE
workload.kueue.x-k8s.io/job-sleep-high-8de71     test    test          True                  5h12m
workload.kueue.x-k8s.io/job-sleep-normal-1b4d8   test                                        5h12m

NAME                     STATUS      COMPLETIONS   DURATION   AGE
job.batch/sleep-high     Running     0/3           8s         5h12m
job.batch/sleep-normal   Suspended   0/3                      5h12m

NAME                     READY   STATUS    RESTARTS   AGE
pod/sleep-high-0-spsfk   1/1     Running   0          8s
pod/sleep-high-1-wjfx9   1/1     Running   0          8s
pod/sleep-high-2-vcxfk   1/1     Running   0          8s
$ kubectl get lq,cq
NAME                             CLUSTERQUEUE   PENDING WORKLOADS   ADMITTED WORKLOADS
localqueue.kueue.x-k8s.io/test   test           1                   1

NAME                               COHORT   PENDING WORKLOADS
clusterqueue.kueue.x-k8s.io/test            1
```

可以看到排在前面的高优先级作业先运行了。

## 实验三、不开启抢占

保持配置不变，清空所有作业，然后先提交作业 sleep-normal, 再提交作业 sleep-high, 查看状态：

```console
$ kubectl get job,wl,po
NAME                     STATUS      COMPLETIONS   DURATION   AGE
job.batch/sleep-high     Suspended   0/3                      16s
job.batch/sleep-normal   Running     0/3           24s        24s

NAME                                             QUEUE   RESERVED IN   ADMITTED   FINISHED   AGE
workload.kueue.x-k8s.io/job-sleep-high-f9455     test                                        16s
workload.kueue.x-k8s.io/job-sleep-normal-dc237   test    test          True                  24s

NAME                       READY   STATUS    RESTARTS   AGE
pod/sleep-normal-0-vwdb2   1/1     Running   0          24s
pod/sleep-normal-1-lkf72   1/1     Running   0          24s
pod/sleep-normal-2-dnlkl   1/1     Running   0          24s
$ kubectl kueue list wl
NAME                     JOB TYPE   JOB NAME       LOCALQUEUE   CLUSTERQUEUE   STATUS     POSITION IN QUEUE   EXEC TIME   AGE
job-sleep-high-f9455     job        sleep-high     test         test           PENDING    0                               4s
job-sleep-normal-dc237   job        sleep-normal   test         test           ADMITTED                       15s         12s
```

可见当作业运行以后，即使队列中的作业优先级更高也不能再运行。

## 实验四、开启抢占

Kueue 的作业抢占情形较为复杂，此处仅研究 `ClusterQueue` 队列内的抢占，需要正确设置其 `spec.preemption` 属性：

:::{literalinclude} /_files/macos/console/kubectl/get_cq_preempt.txt
:diff: /_files/macos/console/kubectl/get_cq_cpu_4.txt
:::

步骤同实验三。先提交作业 `sleep-normal`:

```console
$ kubectl apply -f sleep_job_kueue.yaml 
job.batch/sleep-normal created
$ kubectl get job
NAME           STATUS    COMPLETIONS   DURATION   AGE
sleep-normal   Running   0/3           3s         3s 
```

观察状态确保作业已运行。然后提交作业 `sleep-high`:

```console
$ kubectl apply -f sleep_job_kueue_high.yaml
job.batch/sleep-high created
$ kubectl get job,wl,po
NAME                     STATUS      COMPLETIONS   DURATION   AGE
job.batch/sleep-high     Running     0/3           6s         6s
job.batch/sleep-normal   Suspended   0/3                      18s

NAME                                             QUEUE   RESERVED IN   ADMITTED   FINISHED   AGE
workload.kueue.x-k8s.io/job-sleep-high-8fef6     test    test          True                  6s
workload.kueue.x-k8s.io/job-sleep-normal-7c41c   test                  False                 18s

NAME                     READY   STATUS    RESTARTS   AGE
pod/sleep-high-0-dvtjd   1/1     Running   0          6s
pod/sleep-high-1-wp7kg   1/1     Running   0          6s
pod/sleep-high-2-2d4td   1/1     Running   0          6s
$ kubectl get lq,cq    
NAME                             CLUSTERQUEUE   PENDING WORKLOADS   ADMITTED WORKLOADS
localqueue.kueue.x-k8s.io/test   test           1                   1

NAME                               COHORT   PENDING WORKLOADS
clusterqueue.kueue.x-k8s.io/test            1
$ kubectl kueue list wl
NAME                     JOB TYPE   JOB NAME       LOCALQUEUE   CLUSTERQUEUE   STATUS     POSITION IN QUEUE   EXEC TIME   AGE
job-sleep-high-8fef6     job        sleep-high     test         test           ADMITTED                       26s         23s
job-sleep-normal-7c41c   job        sleep-normal   test         test           PENDING    0                               35s
```

可以看到已经运行的默认优先级作业被挂起，其所有 Pod 被杀死，高优先级作业抢先运行。

## 实验五、Backfill

ClusterQueue 的默认调度策略为 `BestEffortFIFO`, 如果排在前面的作业不能调度，允许后面满足资源额度限制的作业先调度，即 backfill.

将以上作业的并行度修改为 `5`:

:::{literalinclude} /_files/macos/workspace/k8s/kueue/sleep_job_kueue_big.yaml
:diff: /_files/macos/workspace/k8s/kueue/sleep_job_kueue.yaml
:::

然后提交。因为队列只有 4 个 CPU, 所以作业被挂起：

```console
$ kubectl get job
NAME        STATUS      COMPLETIONS   DURATION   AGE
sleep-big   Suspended   0/5                      6s
$ kubectl get cq -owide
NAME   COHORT   STRATEGY         PENDING WORKLOADS   ADMITTED WORKLOADS
test            BestEffortFIFO   1
```

现在提交原来并行度为 3 的作业。查看状态：

```console
NAME           STATUS      COMPLETIONS   DURATION   AGE
$ kubectl get job
sleep-big      Suspended   0/5                      9m20s
sleep-normal   Running     0/3           10s        10s
$ kubectl get cq -owide
NAME   COHORT   STRATEGY         PENDING WORKLOADS   ADMITTED WORKLOADS
test            BestEffortFIFO   1                   1
```

可见后提交的作业确实先提交运行了。
