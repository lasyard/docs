# Topology, ResourceFlavor, ClusterQueue, LocalQueue

Install kueue first, see <https://kueue.sigs.k8s.io/>.

```sh
vi topology_rf_cq_lq.yaml
```

:::{literalinclude} /_files/macos/work/k8s/topology_rf_cq_lq.yaml
:language: yaml
:class: file-content
:::

:::{note}
For `ResourceFlavor`, At least one of `nodeLabels` is required if `topologyName` is set.
:::

```console
$ kubectl create -f topology_rf_cq_lq.yaml
topology.kueue.x-k8s.io/default created
resourceflavor.kueue.x-k8s.io/default created
clusterqueue.kueue.x-k8s.io/test-cq created
localqueue.kueue.x-k8s.io/test-lq created
```

:::{literalinclude} /_files/macos/console/kubectl/get_topology_rf_cq_lq.txt
:language: console
:::
