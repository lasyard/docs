# LocalQueue

Create a cluster queue first, see <project:clusterqueue.md>

```sh
vi test_lq.yaml
```

:::{literalinclude} /_files/macos/work/k8s/test_lq.yaml
:language: yaml
:class: file-content
:::

```console
$ kubectl create -f test_lq.yaml  
localqueue.kueue.x-k8s.io/test-lq created
```

:::{literalinclude} /_files/macos/console/kubectl/get_lq.txt
:language: console
:::
