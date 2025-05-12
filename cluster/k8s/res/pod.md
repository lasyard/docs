# Pod

Create file `sleep_po.yaml`:

:::{literalinclude} /_files/macos/workspace/k8s/sleep_po.yaml
:language: yaml
:::

Apply to the cluster:

```console
$ kubectl apply -f sleep_po.yaml
pod/sleep created
```

:::{note}
The default value of `spec.restartPolicy` is `Always`, which makes the pod restart again and again.
:::

Watch events:

```console
$ kubectl get po sleep -owide -w
NAME    READY   STATUS              RESTARTS   AGE   IP       NODE     NOMINATED NODE   READINESS GATES
sleep   0/1     ContainerCreating   0          0s    <none>   las1     <none>           <none>
sleep   0/1     ContainerCreating   0          1s    <none>   las1     <none>           <none>
sleep   1/1     Running             0          1s    192.168.135.2   las1     <none>           <none>
sleep   0/1     Completed           0          61s   192.168.135.2   las1     <none>           <none>
sleep   0/1     Completed           0          62s   192.168.135.2   las1     <none>           <none>
sleep   0/1     Completed           0          63s   192.168.135.2   las1     <none>           <none>
sleep   0/1     Completed           0          7m18s   192.168.135.2   las1     <none>           <none>
sleep   0/1     Completed           0          7m18s   192.168.135.2   las1     <none>           <none>
```

The last two lines of output have not be produced until we terminate it on another console with:

```console
$ kubectl delete po sleep
pod "sleep" deleted
```
