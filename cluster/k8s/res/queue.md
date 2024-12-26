# Queue

Install volcano plugin first, see <project:../volcano.md>.

```sh
vi test_q.yaml
```

:::{literalinclude} /_files/macos/work/k8s/test_q.yaml
:language: yaml
:class: file-content
:::

```console
$ kubectl create -f test_q.yaml
queue.scheduling.volcano.sh/test created
```

Check it:

:::{literalinclude} /_files/macos/console/kubectl/get_q.txt
:language: console
:::
