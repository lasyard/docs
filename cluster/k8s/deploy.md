# Deploy Kubernetes with kubeadm

This document is for Ubuntu 22.04.

## Prerequisites

### Install packages

Install packages on each node according their roles. See "<project:install.md>".

### Install containerd

`containerd.io` is released by docker, see "<project:/cluster/docker/install.md>" for how to add docker repository.

After adding the repository and `apt update`, install:

```console
$ sudo apt install -y containerd.io
```

### Pull images

Prepare a configuration file for `kubeadm`:

```console
$ kubeadm config print init-defaults > kubeadm_init.yaml
```

Edit the file `kubeadm_init.yaml`:

:::{literalinclude} /_files/ubuntu/workspace/kubeadm_init.yaml
:diff: /_files/ubuntu/workspace/kubeadm_init.yaml.orig
:::

Pull the required images before initializing the cluster:

```console
$ sudo kubeadm config images pull --config kubeadm_init.yaml
[config/images] Pulled registry.aliyuncs.com/google_containers/kube-apiserver:v1.32.0
[config/images] Pulled registry.aliyuncs.com/google_containers/kube-controller-manager:v1.32.0
[config/images] Pulled registry.aliyuncs.com/google_containers/kube-scheduler:v1.32.0
[config/images] Pulled registry.aliyuncs.com/google_containers/kube-proxy:v1.32.0
[config/images] Pulled registry.aliyuncs.com/google_containers/coredns:v1.11.3
[config/images] Pulled registry.aliyuncs.com/google_containers/pause:3.10
[config/images] Pulled registry.aliyuncs.com/google_containers/etcd:3.5.16-0
```

### Configure containerd

Edit `/etc/containerd/config.toml` to enable `cri` plugin:

:::{literalinclude} /_files/ubuntu/etc/containerd/config.toml.orig
:diff: /_files/ubuntu/etc/containerd/config.toml.orig.orig
:::

Restart `containerd` service to make the config effective, then dump the config:

```console
$ sudo systemctl restart containerd
$ containerd config dump | sudo tee /etc/containerd/config.toml
```

Edit the config again:

:::{literalinclude} /_files/ubuntu/etc/containerd/config.toml
:diff: /_files/ubuntu/etc/containerd/config.toml.dump
:::

Create file `docker.io/hosts.toml` in path `/etc/containerd/certs.d/` to enable docker registry mirror:

:::{literalinclude} /_files/ubuntu/etc/containerd/certs.d/docker.io/hosts.toml
:::

Create file `registry.k8s.io/hosts.toml` in path `/etc/containerd/certs.d/` to enable k8s registry mirror:

:::{literalinclude} /_files/ubuntu/etc/containerd/certs.d/registry.k8s.io/hosts.toml
:::

Then restart the service again to make it effective:

```console
$ sudo systemctl restart containerd
```

If you want to pull images via proxy, you can set envs for the service:

```console
$ sudo systemctl edit --full containerd
```

:::{literalinclude} /_files/ubuntu/etc/systemd/system/containerd.service
:diff: /_files/ubuntu/etc/systemd/system/containerd.service.orig
:::

Do not forget to do this:

```console
$ sudo systemctl daemon-reload
$ sudo systemctl restart containerd
```

:::{note}
Must apply the same config on each node in the cluster.
:::

### Configure networking

Create file `/etc/sysctl.d/10-ipv4-forward.conf`:

:::{literalinclude} /_files/ubuntu/etc/sysctl.d/10-ipv4-forward.conf
:language: ini
:::

Make it effective:

```console
$ sudo sysctl --system
```

Check if it is enabled:

```console
$ sysctl net.ipv4.ip_forward
net.ipv4.ip_forward = 1
```

## Initialize the cluster

Initialize the cluster using the config we edited:

```console
$ sudo kubeadm init --v=5 --config kubeadm_init.yaml
...
Your Kubernetes control-plane has initialized successfully!

To start using your cluster, you need to run the following as a regular user:

  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config

Alternatively, if you are the root user, you can run:

  export KUBECONFIG=/etc/kubernetes/admin.conf

You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
  https://kubernetes.io/docs/concepts/cluster-administration/addons/

Then you can join any number of worker nodes by running the following on each as root:

kubeadm join 10.225.4.51:6443 --token abcdef.0123456789abcdef \
    --discovery-token-ca-cert-hash sha256:9fa0763af09ffb5629e2ecd7f6b301c26e9941afb8013f58fece0b3e9cad1d62 
```

Note the output contains information on how to set kube config and how to join worker nodes to the cluster.

In case of failure, reset the node before retrying:

```console
$ sudo kubeadm reset
```

See <project:teardown.md> to see how to completely remove a cluster.

:::{tip}
This command can also be used to reset the worker nodes if you want to do `join` again.
:::

## Join worker nodes

On other worker nodes, install packages and config as mentioned in "<project:#prerequisites>", then join the cluster using `kubeadm`:

```console
$ sudo kubeadm join 10.225.4.51:6443 --token abcdef.0123456789abcdef --discovery-token-ca-cert-hash sha256:9fa0763af09ffb5629e2ecd7f6b301c26e9941afb8013f58fece0b3e9cad1d62
[preflight] Running pre-flight checks
[preflight] Reading configuration from the "kubeadm-config" ConfigMap in namespace "kube-system"...
[preflight] Use 'kubeadm init phase upload-config --config your-config.yaml' to re-upload it.
[kubelet-start] Writing kubelet configuration to file "/var/lib/kubelet/config.yaml"
[kubelet-start] Writing kubelet environment file with flags to file "/var/lib/kubelet/kubeadm-flags.env"
[kubelet-start] Starting the kubelet
[kubelet-check] Waiting for a healthy kubelet at http://127.0.0.1:10248/healthz. This can take up to 4m0s
[kubelet-check] The kubelet is healthy after 501.468269ms
[kubelet-start] Waiting for the kubelet to perform the TLS Bootstrap

This node has joined the cluster:
* Certificate signing request was sent to apiserver and a response was received.
* The Kubelet was informed of the new secure connection details.

Run 'kubectl get nodes' on the control-plane to see this node join the cluster.
```

:::{note}
If the token is expired, you can generate a new one and get the join command by:

```console
$ kubeadm token create --print-join-command --ttl 24h
```

The expiration time is set to 24 hours as above.
:::

## Install networking

Install the Tigera operator and custom resource definitions:

```console
$ curl -LO https://raw.githubusercontent.com/projectcalico/calico/v3.29.3/manifests/tigera-operator.yaml
$ kubectl create -f tigera-operator.yaml
namespace/tigera-operator created
customresourcedefinition.apiextensions.k8s.io/bgpconfigurations.crd.projectcalico.org created
customresourcedefinition.apiextensions.k8s.io/bgpfilters.crd.projectcalico.org created
customresourcedefinition.apiextensions.k8s.io/bgppeers.crd.projectcalico.org created
customresourcedefinition.apiextensions.k8s.io/blockaffinities.crd.projectcalico.org created
customresourcedefinition.apiextensions.k8s.io/caliconodestatuses.crd.projectcalico.org created
customresourcedefinition.apiextensions.k8s.io/clusterinformations.crd.projectcalico.org created
customresourcedefinition.apiextensions.k8s.io/felixconfigurations.crd.projectcalico.org created
customresourcedefinition.apiextensions.k8s.io/globalnetworkpolicies.crd.projectcalico.org created
customresourcedefinition.apiextensions.k8s.io/globalnetworksets.crd.projectcalico.org created
customresourcedefinition.apiextensions.k8s.io/hostendpoints.crd.projectcalico.org created
customresourcedefinition.apiextensions.k8s.io/ipamblocks.crd.projectcalico.org created
customresourcedefinition.apiextensions.k8s.io/ipamconfigs.crd.projectcalico.org created
customresourcedefinition.apiextensions.k8s.io/ipamhandles.crd.projectcalico.org created
customresourcedefinition.apiextensions.k8s.io/ippools.crd.projectcalico.org created
customresourcedefinition.apiextensions.k8s.io/ipreservations.crd.projectcalico.org created
customresourcedefinition.apiextensions.k8s.io/kubecontrollersconfigurations.crd.projectcalico.org created
customresourcedefinition.apiextensions.k8s.io/networkpolicies.crd.projectcalico.org created
customresourcedefinition.apiextensions.k8s.io/networksets.crd.projectcalico.org created
customresourcedefinition.apiextensions.k8s.io/tiers.crd.projectcalico.org created
customresourcedefinition.apiextensions.k8s.io/adminnetworkpolicies.policy.networking.k8s.io created
customresourcedefinition.apiextensions.k8s.io/apiservers.operator.tigera.io created
customresourcedefinition.apiextensions.k8s.io/imagesets.operator.tigera.io created
customresourcedefinition.apiextensions.k8s.io/installations.operator.tigera.io created
customresourcedefinition.apiextensions.k8s.io/tigerastatuses.operator.tigera.io created
serviceaccount/tigera-operator created
clusterrole.rbac.authorization.k8s.io/tigera-operator created
clusterrolebinding.rbac.authorization.k8s.io/tigera-operator created
deployment.apps/tigera-operator created
```

Install Calico:

```console
$ curl -LO https://raw.githubusercontent.com/projectcalico/calico/v3.29.3/manifests/custom-resources.yaml
$ kubectl create -f custom-resources.yaml
installation.operator.tigera.io/default created
apiserver.operator.tigera.io/default created
```

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

Check the node status:

```console
$ kubectl get nodes
NAME     STATUS   ROLES           AGE    VERSION
las1     Ready    <none>          96m    v1.32.3
las2     Ready    <none>          67m    v1.32.3
las0     Ready    control-plane   125m   v1.32.3
```

Without installing network, the status of node would be `NotReady`.

## Ready

If you want to schedule pod to the control-plane node, you need to remove the taint:

```console
$ kubectl taint node las0 node-role.kubernetes.io/control-plane-
node/las0 untainted
```

Check the cluster version:

```console
$ kubectl version -o yaml
clientVersion:
  buildDate: "2025-03-11T19:58:53Z"
  compiler: gc
  gitCommit: 32cc146f75aad04beaaa245a7157eb35063a9f99
  gitTreeState: clean
  gitVersion: v1.32.3
  goVersion: go1.23.6
  major: "1"
  minor: "32"
  platform: linux/amd64
kustomizeVersion: v5.5.0
serverVersion:
  buildDate: "2024-12-11T17:59:15Z"
  compiler: gc
  gitCommit: 70d3cc986aa8221cd1dfb1121852688902d3bf53
  gitTreeState: clean
  gitVersion: v1.32.0
  goVersion: go1.23.3
  major: "1"
  minor: "32"
  platform: linux/amd64
```

Check cluster info:

```console
$ kubectl cluster-info
Kubernetes control plane is running at https://10.225.4.51:6443
CoreDNS is running at https://10.225.4.51:6443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.
$ kubectl get clusterinfo
NAME      CREATED AT
default   2025-04-18T09:07:51Z
```

Check all deployed services:

```console
$ kubectl get svc -A
NAMESPACE          NAME                              TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)                  AGE
calico-apiserver   calico-api                        ClusterIP   10.108.198.28   <none>        443/TCP                  65m
calico-system      calico-kube-controllers-metrics   ClusterIP   None            <none>        9094/TCP                 23m
calico-system      calico-typha                      ClusterIP   10.103.236.57   <none>        5473/TCP                 65m
default            kubernetes                        ClusterIP   10.96.0.1       <none>        443/TCP                  132m
kube-system        kube-dns                          ClusterIP   10.96.0.10      <none>        53/UDP,53/TCP,9153/TCP   132m
```
