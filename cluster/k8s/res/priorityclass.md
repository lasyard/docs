# PriorityClass

```sh
vi high_pc.yaml
```

:::{literalinclude} /_files/macos/work/k8s/high_pc.yaml
:language: yaml
:class: file-content
:::

```console
$ kubectl create -f high_pc.yaml
priorityclass.scheduling.k8s.io/high-priority created
```

Check it:

:::{literalinclude} /_files/macos/console/kubectl/get_pc.txt
:language: console
:::
