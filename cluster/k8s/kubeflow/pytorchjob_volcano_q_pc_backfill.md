# 在 Kubeflow 作业中使用 Volcano 调度器队列、优先级和 backfill 功能

## 实验内容

首先在 k8s 中创建一个 PriorityClass:

```console
$ kubectl apply -f high_pc.yaml
priorityclass.scheduling.k8s.io/high-priority created
```

其定义如下：

:::{literalinclude} /_files/macos/workspace/k8s/high_pc.yaml
:::

默认的优先级值为 0, 因此以上优先级高于默认。

创建一个 Volcano 队列：

```console
$ kubectl apply -f test_q_8g.yaml 
queue.scheduling.volcano.sh/test created
```

其定义如下：

:::{literalinclude} /_files/macos/workspace/k8s/kubeflow/test_q_8g.yaml
:::

使用如下 PyTorchJob 定义：

:::{literalinclude} /_files/macos/workspace/k8s/kubeflow/pytorchjob_q_test.yaml
:::

其中与 Volcano 队列和优先级相关的设置都放在 `.spec.runPolicy.schedulingPolicy` 下面。

### 优先调度实验

首先提交一个作业：

```console
$ kubectl create -f pytorchjob_q_test.yaml
pytorchjob.kubeflow.org/job-6wgnj created
```

当它调度后，队列的容量已不足，这时再创建一个默认优先级作业：

```console
$ yq 'del(.spec.runPolicy.schedulingPolicy.priorityClass)' pytorchjob_q_test.yaml | kubectl create -f -
pytorchjob.kubeflow.org/job-2jmz2 created
```

随后再创建一个高优先级作业：

```console
$ kubectl create -f pytorchjob_q_test.yaml
pytorchjob.kubeflow.org/job-58cjb created
```

这时后创建的两个作业都在排队状态。

监视 PyTorchJob 状态：

```console
$ kubectl get pytorchjob -w                                                                      
NAME        STATE   AGE
job-6wgnj           0s
job-6wgnj   Created   0s
job-6wgnj   Created   1s
job-6wgnj   Running   3s
job-6wgnj   Running   6s
job-6wgnj   Running   6s
job-6wgnj   Running   6s
job-2jmz2             0s
job-2jmz2   Created   0s
job-2jmz2   Created   1s
job-58cjb             0s
job-58cjb   Created   0s
job-58cjb   Created   1s
job-58cjb   Created   2s
job-6wgnj   Succeeded   34s
job-6wgnj   Succeeded   35s
job-58cjb   Running     20s
job-58cjb   Running     24s
job-58cjb   Running     24s
job-58cjb   Running     24s
job-58cjb   Running     24s
job-58cjb   Succeeded   52s
job-58cjb   Succeeded   52s
job-2jmz2   Running     56s
job-2jmz2   Running     59s
job-2jmz2   Running     59s
job-2jmz2   Running     59s
job-2jmz2   Running     59s
job-2jmz2   Succeeded   87s
job-2jmz2   Succeeded   87s
```

监视 PodGroup 状态：

```console
$ kubectl get podgroup -owide -w
NAME        STATUS   MINMEMBER   RUNNINGS   AGE   QUEUE
job-6wgnj            6                      0s    test
job-6wgnj   Inqueue   6                      0s    test
job-6wgnj   Running   6                      2s    test
job-6wgnj   Running   6           1          4s    test
job-6wgnj   Running   6           6          7s    test
job-2jmz2             6                      0s    test
job-2jmz2   Inqueue   6                      1s    test
job-2jmz2   Inqueue   6                      2s    test
job-58cjb             6                      0s    test
job-58cjb   Inqueue   6                      1s    test
job-58cjb   Inqueue   6                      2s    test
job-6wgnj   Running   6           6          35s   test
job-58cjb   Running   6                      19s   test
job-58cjb   Running   6           1          21s   test
job-58cjb   Running   6           4          24s   test
job-58cjb   Running   6           6          25s   test
job-58cjb   Running   6           6          52s   test
job-2jmz2   Running   6                      54s   test
job-2jmz2   Running   6           1          56s   test
job-2jmz2   Running   6           5          59s   test
job-2jmz2   Running   6           6          60s   test
job-2jmz2   Running   6           6          87s   test
```

可以看出队列中高优先级的作业先被调度了。

### backfill 实验

首先提交一个作业：

```console
$ kubectl create -f pytorchjob_q_test.yaml
pytorchjob.kubeflow.org/job-gtps2 created
```

当它调度后，队列的容量已不足，这时再创建一个作业：

```console
$ kubectl create -f pytorchjob_q_test.yaml
pytorchjob.kubeflow.org/job-xjhtm created
```

这个作业应该处于排队状态。随后再创建一个需要资源较少的作业：

```console
$ yq 'del(.spec.pytorchReplicaSpecs.Worker)' pytorchjob_q_test.yaml | kubectl create -f -
pytorchjob.kubeflow.org/job-vr5xc created
```

注意：Worker 的数量最少为 1, 但是可以把整个 Worker 字段去掉。

监视 PyTorchJob 状态：

```console
$ kubectl get pytorchjob -w                                                                      
NAME        STATE   AGE
job-gtps2           0s
job-gtps2   Created   0s
job-gtps2   Created   0s
job-gtps2   Running   2s
job-gtps2   Running   4s
job-gtps2   Running   4s
job-gtps2   Running   4s
job-gtps2   Running   6s
job-xjhtm             0s
job-xjhtm   Created   0s
job-xjhtm   Created   1s
job-vr5xc             1s
job-vr5xc   Created   1s
job-vr5xc   Created   1s
job-vr5xc   Running   3s
job-gtps2   Succeeded   33s
job-gtps2   Succeeded   33s
job-xjhtm   Running     27s
job-xjhtm   Running     28s
job-xjhtm   Running     28s
job-xjhtm   Running     28s
job-xjhtm   Running     29s
job-xjhtm   Running     30s
job-vr5xc   Succeeded   34s
job-xjhtm   Succeeded   58s
job-xjhtm   Succeeded   58s
```

监视 PodGroup 状态：

```console
$ kubectl get podgroup -owide -w
NAME        STATUS   MINMEMBER   RUNNINGS   AGE   QUEUE
job-gtps2            6                      0s    test
job-gtps2   Inqueue   6                      0s    test
job-gtps2   Running   6                      1s    test
job-gtps2   Running   6           1          2s    test
job-gtps2   Running   6           3          4s    test
job-gtps2   Running   6           5          5s    test
job-gtps2   Running   6           6          6s    test
job-xjhtm             6                      0s    test
job-xjhtm   Inqueue   6                      1s    test
job-xjhtm   Inqueue   6                      2s    test
job-vr5xc             1                      0s    test
job-vr5xc   Inqueue   1                      0s    test
job-vr5xc   Running   1                      1s    test
job-vr5xc   Running   1           1          2s    test
job-xjhtm   Inqueue   6                      10s   test
job-gtps2   Running   6           6          33s   test
job-xjhtm   Running   6                      26s   test
job-xjhtm   Running   6           1          27s   test
job-xjhtm   Running   6           5          29s   test
job-xjhtm   Running   6           6          31s   test
job-vr5xc   Running   1           1          33s   test
job-xjhtm   Running   6           6          58s   test
```

可以看出队列中排在后面但是资源能够容纳的作业被先调度了。

## 结论

- Kubeflow 作业支持定义 Volcano 的队列和优先级
- 队列中高优先级的作业将先于低优先级的作业运行
- backfill 功能有效，当队列的资源不足以调度下一个作业时，Volcano 会查找队列后面消耗资源较少能够被调度的作业提前调度
