# Calico

<https://www.tigera.io/project-calico/>

## Install

Download the Tigera operator definitions:

```console
$ curl -Lo tigera-operator-3.32.2.yaml https://raw.githubusercontent.com/projectcalico/calico/v3.32.2/manifests/tigera-operator.yaml
```

Install it:

```console
$ kubectl create -f tigera-operator-3.32.2.yaml
namespace/tigera-operator created
serviceaccount/tigera-operator created
clusterrole.rbac.authorization.k8s.io/tigera-operator-secrets created
clusterrole.rbac.authorization.k8s.io/tigera-operator created
clusterrolebinding.rbac.authorization.k8s.io/tigera-operator created
rolebinding.rbac.authorization.k8s.io/tigera-operator-secrets created
deployment.apps/tigera-operator created
```

Download the Calico definitions:

```console
$ curl -Lo custom-resources-3.32.2.yaml https://raw.githubusercontent.com/projectcalico/calico/v3.32.2/manifests/custom-resources.yaml
```

Install it:

```console
$ kubectl create -f custom-resources-3.32.2.yaml
installation.operator.tigera.io/default created
apiserver.operator.tigera.io/default created
goldmane.operator.tigera.io/default created
whisker.operator.tigera.io/default created
```

> [!IMPORTANT]
> The CIDR setting of the Installation object must be the same as the Pod CIDR setting of the cluster.

Wait until all these pods are in the "Running" state:

```console
$ watch kubectl get pods -n calico-system
...
NAME                                       READY   STATUS    RESTARTS   AGE
calico-kube-controllers-548dddd6d4-kbdhq   1/1     Running   0          55m
calico-node-42drn                          1/1     Running   0          55m
calico-node-tvf4f                          1/1     Running   0          55m
calico-node-znwtb                          1/1     Running   0          55m
calico-typha-7cf7ffb6b-44vpb               1/1     Running   0          55m
calico-typha-7cf7ffb6b-bd46j               1/1     Running   0          55m
csi-node-driver-5kxdw                      2/2     Running   0          55m
csi-node-driver-kt585                      2/2     Running   0          55m
csi-node-driver-ljr6d                      2/2     Running   0          55m
```

## Uninstall

```console
$ kubectl delete -f custom-resources-3.32.2.yaml 
installation.operator.tigera.io "default" deleted
apiserver.operator.tigera.io "default" deleted
goldmane.operator.tigera.io "default" deleted
whisker.operator.tigera.io "default" deleted
$ kubectl delete -f tigera-operator-3.32.2.yaml 
namespace "tigera-operator" deleted
serviceaccount "tigera-operator" deleted from tigera-operator namespace
clusterrole.rbac.authorization.k8s.io "tigera-operator-secrets" deleted
clusterrole.rbac.authorization.k8s.io "tigera-operator" deleted
clusterrolebinding.rbac.authorization.k8s.io "tigera-operator" deleted
rolebinding.rbac.authorization.k8s.io "tigera-operator-secrets" deleted from tigera-operator namespace
deployment.apps "tigera-operator" deleted from tigera-operator namespace
```

Delete links created by Calico:

```console
$ sudo ip link delete tunl0
$ sudo ip link delete vxlan.calico
$ for i in $(ip -o link | awk -F': ' '/cali/{print $2}' | cut -d@ -f1); do sudo ip link delete "$i"; done
```

Delete CNI configs:

```console
$ sudo rm -f /etc/cni/net.d/10-calico.conflist /etc/cni/net.d/calico-kubeconfig
```

Delete related binaries:

```console
$ sudo rm -f /opt/cni/bin/calico /opt/cni/bin/calico-ipam
```

Delete other runtime files:

```console
$ sudo rm -rf /var/lib/calico /var/run/calico /var/log/calico
```

Restart the host to clear the iptable rules.
