# Job

Create file `sleep_job.yaml`

:::{literalinclude} /_files/macos/workspace/k8s/sleep_job.yaml
:::

Apply to the cluster:

```console
$ kubectl create -f sleep_job.yaml
job.batch/sleep created
```

Watch events:

```console
$ kubectl get job sleep -owide -w
NAME    STATUS    COMPLETIONS   DURATION   AGE   CONTAINERS      IMAGES                 SELECTOR
sleep   Running   0/3           0s         0s    busybox-sleep   busybox:1.37.0-glibc   batch.kubernetes.io/controller-uid=4b31a55e-d6b4-450f-ab0b-79b0689efc52
sleep   Running   0/3           1s         1s    busybox-sleep   busybox:1.37.0-glibc   batch.kubernetes.io/controller-uid=4b31a55e-d6b4-450f-ab0b-79b0689efc52
sleep   Running   0/3           2s         2s    busybox-sleep   busybox:1.37.0-glibc   batch.kubernetes.io/controller-uid=4b31a55e-d6b4-450f-ab0b-79b0689efc52
sleep   Running   0/3           62s        62s   busybox-sleep   busybox:1.37.0-glibc   batch.kubernetes.io/controller-uid=4b31a55e-d6b4-450f-ab0b-79b0689efc52
sleep   Running   2/3           63s        63s   busybox-sleep   busybox:1.37.0-glibc   batch.kubernetes.io/controller-uid=4b31a55e-d6b4-450f-ab0b-79b0689efc52
sleep   Running   3/3           64s        64s   busybox-sleep   busybox:1.37.0-glibc   batch.kubernetes.io/controller-uid=4b31a55e-d6b4-450f-ab0b-79b0689efc52
sleep   Complete   3/3           64s        64s   busybox-sleep   busybox:1.37.0-glibc   batch.kubernetes.io/controller-uid=4b31a55e-d6b4-450f-ab0b-79b0689efc52
```

If we list the resources when the job was running:

```console
$ kubectl get job,po -owide
NAME              STATUS    COMPLETIONS   DURATION   AGE   CONTAINERS      IMAGES                 SELECTOR
job.batch/sleep   Running   0/3           37s        37s   busybox-sleep   busybox:1.37.0-glibc   batch.kubernetes.io/controller-uid=4b31a55e-d6b4-450f-ab0b-79b0689efc52

NAME                READY   STATUS    RESTARTS   AGE   IP               NODE     NOMINATED NODE   READINESS GATES
pod/sleep-0-hnf55   1/1     Running   0          37s   192.168.135.15   las1     <none>           <none>
pod/sleep-1-vkj5r   1/1     Running   0          37s   192.168.5.219    las2     <none>           <none>
pod/sleep-2-6x526   1/1     Running   0          37s   192.168.5.220    las2     <none>           <none>
```

## Schedule to the same node using pod affinity

Change the job spec:

:::{literalinclude} /_files/macos/workspace/k8s/sleep_job_pod_affinity.yaml
:diff: /_files/macos/workspace/k8s/sleep_job.yaml
:::

After submitting, all pods are scheduled to the same node:

```console
$ kubectl get po -owide
NAME            READY   STATUS    RESTARTS   AGE   IP               NODE   NOMINATED NODE   READINESS GATES
sleep-0-zvz88   1/1     Running   0          4s    192.168.185.26   las3   <none>           <none>
sleep-1-sd5v5   1/1     Running   0          4s    192.168.185.35   las3   <none>           <none>
sleep-2-mbms6   1/1     Running   0          4s    192.168.185.54   las3   <none>           <none>
```
