# ClusterQueue

Create a resource flavor first, see <project:resourceflavor.md>.

```sh
vi test_cq.yaml
```

:::{literalinclude} /_files/macos/work/k8s/test_cq.yaml
:language: yaml
:class: file-content
:::

```console
$ kubectl create -f test_cq.yaml
clusterqueue.kueue.x-k8s.io/test-cq created
```

:::{literalinclude} /_files/macos/console/kubectl/get_cq_owide.txt
:language: console
:::
