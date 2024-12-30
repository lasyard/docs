# Topology

Install kueue first, see <https://kueue.sigs.k8s.io/>.

```sh
vi default_topology.yaml
```

:::{literalinclude} /_files/macos/work/k8s/default_topology.yaml
:language: yaml
:class: file-content
:::

```console
$ kubectl create -f default_topology.yaml 
topology.kueue.x-k8s.io/default created
```

:::{literalinclude} /_files/macos/console/kubectl/get_topology.txt
:language: console
:::
