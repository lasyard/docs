# Volcano Job

Create file `test_q.yaml` for a volcano queue:

:::{literalinclude} /_files/macos/workspace/k8s/test_q.yaml
:language: yaml
:::

Apply to the cluster:

```console
$ kubectl apply -f test_q.yaml
queue.scheduling.volcano.sh/test created
```

Volcano job use `PriorityClass` to specify priority, so create file `high_pc.yaml` for it:

:::{literalinclude} /_files/macos/workspace/k8s/high_pc.yaml
:language: yaml
:::

Apply to the cluster:

```console
$ kubectl apply -f high_pc.yaml
priorityclass.scheduling.k8s.io/high-priority created
```

Now create file `sleep_vj.yaml`:

:::{literalinclude} /_files/macos/workspace/k8s/sleep_vj.yaml
:language: yaml
:::

Apply to the cluster:

```console
$ kubectl apply -f sleep_vj.yaml
job.batch.volcano.sh/sleep created
```

:::{note}
The job will be in `PENDING` state if the underlying pods were not running succcessfuly, which may not caused by lack of resources.
:::

Watch events:

```console
$ kubectl get vj sleep -owide -w
NAME    STATUS    MINAVAILABLE   RUNNINGS   AGE   QUEUE
sleep   Pending   3                         0s    test
sleep   Pending   3                         1s    test
sleep   Pending   3              1          2s    test
sleep   Pending   3              2          3s    test
sleep   Running   3              3          3s    test
sleep   Running   3              2          64s   test
sleep   Running   3              1          64s   test
sleep   Completing   3                         64s   test
sleep   Completed    3                         64s   test
sleep   Completed    3                         64s   test
```

If we list the resources when the job was running:

```console
$ kubectl get vj,pg,po -owide
NAME                         STATUS    MINAVAILABLE   RUNNINGS   AGE   QUEUE
job.batch.volcano.sh/sleep   Running   3              3          13s   test

NAME                                                                        STATUS    MINMEMBER   RUNNINGS   AGE   QUEUE
podgroup.scheduling.volcano.sh/sleep-d6693086-b400-43c7-a0d9-baf606ff3479   Running   3           3          13s   test

NAME                     READY   STATUS    RESTARTS   AGE   IP               NODE     NOMINATED NODE   READINESS GATES
pod/sleep-sleep-task-0   1/1     Running   0          13s   192.168.5.203    k8cpu1   <none>           <none>
pod/sleep-sleep-task-1   1/1     Running   0          13s   192.168.135.17   k8cpu0   <none>           <none>
pod/sleep-sleep-task-2   1/1     Running   0          13s   192.168.135.16   k8cpu0   <none>           <none>
```

Delete the job:

```console
$ kubectl delete vj sleep-job
job.batch.volcano.sh "sleep" deleted
```

:::{note}
Delete the job will also delete all task pods.
:::
