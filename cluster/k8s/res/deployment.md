# Deployment

Create file `sleep_deploy.yaml`:

:::{literalinclude} /_files/macos/workspace/k8s/sleep_deploy.yaml
:::

:::{note}

- `restartPolicy` must be `Always`, which is the default value
- `selector` must be set and match the labels of template

:::

Apply to the cluster:

```console
$ kubectl apply -f sleep_deploy.yaml
deployment.apps/sleep created
```

Watch events:

```console
$ kubectl get deploy sleep -owide -w
NAME    READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS      IMAGES                 SELECTOR
sleep   0/3     3            0           0s    sleep-busybox   busybox:1.37.0-glibc   app=sleep
sleep   1/3     3            1           1s    sleep-busybox   busybox:1.37.0-glibc   app=sleep
sleep   2/3     3            2           1s    sleep-busybox   busybox:1.37.0-glibc   app=sleep
sleep   3/3     3            3           1s    sleep-busybox   busybox:1.37.0-glibc   app=sleep
sleep   2/3     3            2           61s   sleep-busybox   busybox:1.37.0-glibc   app=sleep
sleep   1/3     3            1           61s   sleep-busybox   busybox:1.37.0-glibc   app=sleep
sleep   0/3     3            0           61s   sleep-busybox   busybox:1.37.0-glibc   app=sleep
sleep   1/3     3            1           62s   sleep-busybox   busybox:1.37.0-glibc   app=sleep
sleep   2/3     3            2           62s   sleep-busybox   busybox:1.37.0-glibc   app=sleep
sleep   3/3     3            3           62s   sleep-busybox   busybox:1.37.0-glibc   app=sleep
```

Note the pods exited after 1min and restarted.

If we list the resources when the deployment was 3/3 ready:

```console
$ kubectl get deploy,rs,po -owide
NAME                    READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS      IMAGES                 SELECTOR
deployment.apps/sleep   3/3     3            3           13s   sleep-busybox   busybox:1.37.0-glibc   app=sleep

NAME                               DESIRED   CURRENT   READY   AGE   CONTAINERS      IMAGES                 SELECTOR
replicaset.apps/sleep-84fddfd8d6   3         3         3       13s   sleep-busybox   busybox:1.37.0-glibc   app=sleep,pod-template-hash=84fddfd8d6

NAME                         READY   STATUS    RESTARTS   AGE   IP               NODE     NOMINATED NODE   READINESS GATES
pod/sleep-84fddfd8d6-9w8s2   1/1     Running   0          13s   192.168.135.7    las1     <none>           <none>
pod/sleep-84fddfd8d6-mvpjk   1/1     Running   0          13s   192.168.182.25   las3     <none>           <none>
pod/sleep-84fddfd8d6-zjpgp   1/1     Running   0          13s   192.168.5.213    las2     <none>           <none>
```
