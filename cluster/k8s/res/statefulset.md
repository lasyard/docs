# StatefulSet

```sh
vi sleep_sts.yaml
```

:::{literalinclude} /_files/macos/work/k8s/sleep_sts.yaml
:language: yaml
:class: file-content
:::

:::{note}

- `restartPolicy` must be `Always`, the default value
- `selector` must be set and match the labels of template

:::

```console
$ kubectl create -f sleep_sts.yaml
statefulset.apps/sleep-sts created
```

Watch events:

:::{literalinclude} /_files/macos/console/kubectl/get_sts_sleep_owide_w.txt
:language: console
:::

If we list the pods when the statefulset was 3/3 ready:

:::{literalinclude} /_files/macos/console/kubectl/get_po_owide_sts_sleep.txt
:language: console
:::
