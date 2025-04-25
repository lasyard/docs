# Teardown Kubernetes Cluster

For every node do:

```console
$ kubectl drain k8cpu0 --delete-emptydir-data --force --ignore-daemonsets
...
node/k8cpu0 drained
$ kubectl delete node k8cpu0
node "k8cpu0" deleted
```

You may need to mannully delete/uninstall something like Deployments/Daemonsets.

After all nodes are deleted from the cluster, run `sudo kubeadm reset` on each node.
