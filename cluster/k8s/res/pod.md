# Pod

```sh
vi sleep_po.yaml
```

:::{literalinclude} /_files/macos/work/k8s/sleep_po.yaml
:language: yaml
:class: file-content
:::

```console
$ kubectl create -f sleep_po.yaml
pod/sleep-po created
```

:::{note}
The default value of `spec.restartPolicy` is `Always`, which makes the pod restart again and again.
:::

Watch events:

:::{literalinclude} /_files/macos/console/kubectl/get_po_sleep_owide_w.txt
:language: console
:::

The last lines of output is produced for we terminate it on another console with:

```sh
kubectl delete po sleep-po
```
