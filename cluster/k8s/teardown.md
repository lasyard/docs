# Teardown Kubernetes Cluster

For every node do:

```console
$ kubectl drain las1 --delete-emptydir-data --force --ignore-daemonsets
...
node/las1 drained
$ kubectl delete node las1
node "las1" deleted
```

You may need to mannully delete/uninstall something like Deployments/Daemonsets.

After all nodes are deleted from the cluster, run `sudo kubeadm reset` on each node.
