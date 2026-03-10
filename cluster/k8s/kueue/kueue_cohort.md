# Kueue 队列在 Cohort 内的资源借用与收回

## 准备工作

创建 ResourceFlavor, Cohort 以及两个队列：

:::{literalinclude} /_files/macos/workspace/k8s/kueue/test_cohort.yaml
:::

Cohort 本身定义的额度是内部所有队列之外的，因此 Cohort 内的额度分配如下图：

```{mermaid}
pie showData title Cohort 额度分配
"队列 test1": 1
"队列 test2": 1
"额外": 2
```

## 实验一、额度借用与收回

创建作业 test1:

:::{literalinclude} /_files/macos/workspace/k8s/kueue/test1_job.yaml
:::

可见作业 test1 使用了整个 Cohort 包括队列 test2 的额度。

然后创建作业 test2:

:::{literalinclude} /_files/macos/workspace/k8s/kueue/test2_job.yaml
:::

监视作业状态变化：

```console
$ kubectl get job -w
NAME    STATUS    COMPLETIONS   DURATION   AGE
test1   Running   0/4                      0s
test1   Suspended   0/4                      0s
test1   Suspended   0/4                      0s
test1   Running     0/4           0s         0s
test1   Running     0/4           2s         2s
test2   Running     0/1                      0s
test2   Suspended   0/1                      0s
test1   Running     0/4           9s         9s
test1   Running     0/4                      9s
test1   Running     0/4                      9s
test1   Suspended   0/4                      9s
test2   Suspended   0/1                      0s
test2   Running     0/1           0s         0s
test1   Suspended   0/4                      10s
test2   Running     0/1           2s         2s
test2   Running     0/1           33s        33s
test2   SuccessCriteriaMet   1/1           34s        34s
test2   Complete             1/1           34s        34s
test1   Suspended            0/4                      43s
test1   Running              0/4           0s         43s
test1   Running              0/4           2s         45s
test1   Running              0/4           32s        75s
test1   SuccessCriteriaMet   4/4           33s        76s
test1   Complete             4/4           33s        76s

```

监视 Workload 状态变化：

```console
$ kubectl get wl -o wide -w
NAME              QUEUE   RESERVED IN   ADMITTED   FINISHED   AGE
job-test1-f14e1   test1                                       0s
job-test1-f14e1   test1                                       0s
job-test1-f14e1   test1   test1         True                  0s
job-test1-f14e1   test1   test1         True                  2s
job-test2-f2017   test2                                       0s
job-test1-f14e1   test1   test1         True                  9s
job-test2-f2017   test2                                       0s
job-test2-f2017   test2                                       0s
job-test1-f14e1   test1   test1         True                  9s
job-test1-f14e1   test1                 False                 9s
job-test1-f14e1   test1                 False                 9s
job-test2-f2017   test2   test2         True                  0s
job-test1-f14e1   test1                 False                 9s
job-test1-f14e1   test1                 False                 9s
job-test2-f2017   test2   test2         True                  2s
job-test2-f2017   test2   test2         True                  33s
job-test2-f2017   test2   test2         True                  34s
job-test2-f2017   test2                 False      True       34s
job-test2-f2017   test2                 False      True       34s
job-test1-f14e1   test1   test1         True                  43s
job-test1-f14e1   test1   test1         True                  45s
job-test1-f14e1   test1   test1         True                  75s
job-test1-f14e1   test1   test1         True                  76s
job-test1-f14e1   test1                 False      True       76s
job-test1-f14e1   test1                 False      True       76s
```

可以看到作业 test2 提交后，作业 test1 被迫退出。

## 实验二、只能收回本队列额度

现在将作业 test2 的并行度改为 2, 超过队列 test2 的额度：

:::{literalinclude} /_files/macos/workspace/k8s/kueue/test3_job.yaml
:diff: /_files/macos/workspace/k8s/kueue/test2_job.yaml
:::

与实验二步骤相同。监视作业状态变化：

```console
$ kubectl get job -w
NAME    STATUS    COMPLETIONS   DURATION   AGE
test1   Running   0/4                      0s
test1   Suspended   0/4                      0s
test1   Suspended   0/4                      0s
test1   Running     0/4           0s         0s
test1   Running     0/4           2s         2s
test2   Running     0/2                      0s
test2   Suspended   0/2                      0s
test1   Running     0/4           32s        32s
test1   SuccessCriteriaMet   4/4           33s        33s
test1   Complete             4/4           33s        33s
test2   Suspended            0/2                      26s
test2   Running              0/2           0s         26s
test2   Running              0/2           2s         28s
test2   Running              0/2           32s        58s
test2   SuccessCriteriaMet   2/2           33s        59s
test2   Complete             2/2           33s        59s
```

监视 Workload 状态变化：

```console
$ kubectl get wl -o wide -w
NAME              QUEUE   RESERVED IN   ADMITTED   FINISHED   AGE
job-test1-647d2   test1                                       0s
job-test1-647d2   test1                                       0s
job-test1-647d2   test1   test1         True                  0s
job-test1-647d2   test1   test1         True                  2s
job-test2-05e1b   test2                                       0s
job-test2-05e1b   test2                                       0s
job-test2-05e1b   test2                                       0s
job-test1-647d2   test1   test1         True                  32s
job-test1-647d2   test1   test1         True                  33s
job-test2-05e1b   test2                                       26s
job-test1-647d2   test1   test1         True                  33s
job-test2-05e1b   test2   test2         True                  26s
job-test1-647d2   test1                 False      True       33s
job-test1-647d2   test1                 False      True       33s
job-test2-05e1b   test2   test2         True                  28s
job-test2-05e1b   test2   test2         True                  58s
job-test2-05e1b   test2   test2         True                  59s
job-test2-05e1b   test2                 False      True       59s
job-test2-05e1b   test2                 False      True       59s
```

可以看到作业 test2 因为额度不够被挂起了。等作业 test1 完成以后，test2 又可以借用 Cohort 内的资源运行。

以上结果是因为关闭了 `borrowWithinCohort` 功能。如果打开的话，高优先级的作业可以挤掉其他队列里低优先级的作业。
