# StatefulSet

Create file `sleep_sts.yaml`:

:::{literalinclude} /_files/macos/workspace/k8s/sleep_sts.yaml
:language: yaml
:class: file-content
:::

:::{note}

- `restartPolicy` must be `Always`, the default value
- `selector` must be set and match the labels of template

:::

Apply to the cluster:

```console
$ kubectl create -f sleep_sts.yaml
statefulset.apps/sleep created
```

Watch events:

```console
$ kubectl get sts sleep -owide -w
NAME    READY   AGE   CONTAINERS      IMAGES
sleep   0/3     0s    sleep-busybox   busybox:1.37.0-glibc
sleep   1/3     2s    sleep-busybox   busybox:1.37.0-glibc
sleep   2/3     2s    sleep-busybox   busybox:1.37.0-glibc
sleep   3/3     2s    sleep-busybox   busybox:1.37.0-glibc
sleep   2/3     62s   sleep-busybox   busybox:1.37.0-glibc
sleep   1/3     62s   sleep-busybox   busybox:1.37.0-glibc
sleep   0/3     62s   sleep-busybox   busybox:1.37.0-glibc
sleep   1/3     63s   sleep-busybox   busybox:1.37.0-glibc
sleep   2/3     63s   sleep-busybox   busybox:1.37.0-glibc
sleep   3/3     63s   sleep-busybox   busybox:1.37.0-glibc
```

Note the pods exited after 1min and restarted.

If we list the resources when the statefulset was 3/3 ready:

```console
$ kubectl get sts,po -owide
NAME                     READY   AGE   CONTAINERS      IMAGES
statefulset.apps/sleep   3/3     17s   sleep-busybox   busybox:1.37.0-glibc

NAME          READY   STATUS    RESTARTS   AGE   IP               NODE     NOMINATED NODE   READINESS GATES
pod/sleep-0   1/1     Running   0          17s   192.168.135.12   k8cpu0   <none>           <none>
pod/sleep-1   1/1     Running   0          17s   192.168.5.217    k8cpu1   <none>           <none>
pod/sleep-2   1/1     Running   0          17s   192.168.182.29   k8gpu    <none>           <none>
```
