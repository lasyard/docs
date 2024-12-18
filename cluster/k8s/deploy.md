# Kubernetes Deployment

::::{plat} centos
{{ cluster_las }}

Roles of the nodes:

:Control-plane: las0
:Nodes: las0, las1, las2

:::{note}
Linux kernel 4.18 is not supported by kubernetes 1.32.
:::

::::

## Prerequisites

::::{plat} centos
Add repository for `containerd.io`:

```sh
sudo dnf config-manager --add-repo=https://download.docker.com/linux/centos/docker-ce.repo
```

Install required packages:

```sh
sudo dnf install containerd.io iproute-tc
```

Disable SELinux on all nodes, see [SELinux](project:/os/centos/misc.md#disable-selinux).

Disable swap on all nodes, see [Set swap off](project:/os/centos/misc.md#set-swap-off).

Install packages on each node according their roles. See "<project:install.md>".
::::

## Configure networking

```sh
sudo vi /etc/sysctl.d/k8s.conf
```

:::{literalinclude} /_files/centos/etc/sysctl.d/k8s.conf
:language: ini
:class: file-content
:::

Make it effective:

```sh
sudo sysctl --system
```

Check if it is enabled:

```console
$ sysctl net.ipv4.ip_forward
net.ipv4.ip_forward = 1
```

## Configure containerd

Enable cri plugin:

```sh
sudo vi /etc/containerd/config.toml
```

:::{literalinclude} /_files/centos/etc/containerd/config.toml.orig
:diff: /_files/centos/etc/containerd/config.toml.orig.orig
:class: file-content
:::

Then restart containerd service to make the config effective, dump the config and edit it again to change the sandbox image url:

```sh
sudo systemctl restart containerd
containerd config dump | sudo tee /etc/containerd/config.toml
sudo vi /etc/containerd/config.toml
```

:::{literalinclude} /_files/centos/etc/containerd/config.toml
:diff: /_files/centos/etc/containerd/config.toml.dump
:class: file-content
:::

Then restart the service again to make it effective:

```sh
sudo systemctl restart containerd
```

:::{note}
Must apply the same config on each node in the cluster.
:::

## Initialize the cluster

Prepare a configuration file for `kubeadm`:

```sh
kubeadm config print init-defaults > kubeadm_init.yaml
vi kubeadm_init.yaml
```

:::{literalinclude} /_files/centos/work/kubeadm/kubeadm_init.yaml
:diff: /_files/centos/work/kubeadm/kubeadm_init.yaml.orig
:class: file-content
:::

Pull the required images before initializing the cluster:

```sh
sudo kubeadm config images pull --config kubeadm_init.yaml
```

Initialize the cluster:

```sh
sudo kubeadm init --v=5 --config kubeadm_init.yaml
```

The output will contain a join command to add worker nodes, something like:

{.cli-output}

```sh
kubeadm join 172.20.3.73:6443 --token abcdef.0123456789abcdef \
    --discovery-token-ca-cert-hash sha256:083bf8517dbd423a9b6eb4ce7c675d0acd508e428dab11344b6f28019e00af4d 
```

:::{note}
Before join the cluster, some services must be enabled:

```sh
sudo systemctl enable containerd kubelet --now
```

:::

In case of failure, reset the node before retrying:

```sh
sudo kubeadm reset
```

:::{tip}
This command can also clear the kubelet's configuration and certificates on the worker nodes if you want to do `join` again.
:::

Copy configuration files to the home directory to enable `kubectl` access:

```sh
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

Alternatively, if you are the root user, you can directly use the `conf` by setting the `KUBECONFIG` environment variable:

```sh
export KUBECONFIG=/etc/kubernetes/admin.conf
```

You can also copy the `admin.conf` to other nodes to enable kubectl access on them.

Check the cluster version:

:::{literalinclude} /_files/centos/console/kubectl/version.txt
:language: console
:::

Remove the taints on the control plane so that you can schedule pods on it:

:::{literalinclude} /_files/centos/console/kubectl/taint_nodes_all.txt
:language: console
:::

## Install networking

:::{literalinclude} /_files/centos/console/kubectl/create_tigera_operator.txt
:language: console
:::

:::{literalinclude} /_files/centos/console/kubectl/create_custom_resources.txt
:language: console
:::

Wait until all these pods are in the "Running" state:

```sh
watch kubectl get pods -n calico-system
```

## Join the worker nodes

On each worker node, run the `kubeadm join` command from the output of the `kubeadm init`.

Check all nodes are in the "Ready" status:

:::{literalinclude} /_files/centos/console/kubectl/get_nodes.txt
:language: console
:::

Check deployed services:

:::{literalinclude} /_files/centos/console/kubectl/get_services_all.txt
:language: console
:::

Check cluster info:

:::{literalinclude} /_files/centos/console/kubectl/cluster_info.txt
:language: console
:::

:::{literalinclude} /_files/centos/console/kubectl/get_clusterinfo.txt
:language: console
:::
