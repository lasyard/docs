# Kubernetes Deployment

::::{plat} centos
{{ cluster_las }}

Roles of the nodes:

:Control-plane: las1
:Nodes: las1, las2, las3

## Prerequisites

```sh
sudo dnf install containerd.io
sudo dnf install iproute-tc
```

Disable SELinux on all nodes, see [SELinux](project:/os/centos/misc.md#disable-selinux).

Disable swap on all nodes, see [Set swap off](project:/os/centos/misc.md#set-swap-off).

Install packages on each node according their roles. See "<project:install.md>".

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

```sh
sysctl net.ipv4.ip_forward
```

{.cli-output}

```ini
net.ipv4.ip_forward = 1
```

## Configure containerd

Configure containerd to enable the cri plugin (on all nodes):

```sh
containerd config dump > /etc/containerd/config.toml
sudo vi /etc/containerd/config.toml
```

:::{literalinclude} /_files/centos/etc/containerd/config.toml
:diff: /_files/centos/etc/containerd/config.toml.orig
:class: file-content
:::

```sh
sudo systemctl restart containerd
```

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

In case of failure, reset the cluster before retrying:

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

```sh
kubectl version -o yaml
```

:::{literalinclude} /_files/centos/output/kubectl/version.yaml
:language: yaml
:class: cli-output
:::

::::

## Install networking

```sh
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.28.0/manifests/tigera-operator.yaml
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.28.0/manifests/custom-resources.yaml
```

Wait until all these pods are in the "Running" state:

```sh
watch kubectl get pods -n calico-system
```

Remove the taints on the control plane so that you can schedule pods on it:

```sh
kubectl taint nodes --all node-role.kubernetes.io/control-plane-
```

## Join the worker nodes

On each worker node, run the `kubeadm join` command from the output of the `kubeadm init`.

Check all nodes are in the "Ready" status:

```sh
kubectl get nodes
```

:::{literalinclude} /_files/centos/output/kubectl/get_nodes.txt
:language: text
:class: cli-output
:::

Check deployed services:

```sh
kubectl get services -A
```

:::{literalinclude} /_files/centos/output/kubectl/get_services_all.txt
:language: text
:class: cli-output
:::

## Mission Accomplished

```sh
kubectl cluster-info
```

:::{literalinclude} /_files/centos/output/kubectl/cluster_info.txt
:language: text
:class: cli-output
:::

```sh
kubectl get clusterinfo
```

:::{literalinclude} /_files/centos/output/kubectl/get_clusterinfo.txt
:language: text
:class: cli-output
:::

## Install dashboard

Install `helm` first, See "<project:../helm.md>".

Then add `helm` repository:

```sh
helm repo add kubernetes-dashboard https://kubernetes.github.io/dashboard/
```

```sh
helm repo list
```

:::{literalinclude} /_files/centos/output/helm/repo_list.txt
:language: text
:class: cli-output
:::

Install using `helm`:

```sh
helm upgrade --install kubernetes-dashboard kubernetes-dashboard/kubernetes-dashboard --create-namespace --namespace kubernetes-dashboard
```

:::{literalinclude} /_files/centos/output/helm/upgrade_dashboard.txt
:language: text
:class: cli-output
:::

Create a service account for the admin user:

```sh
vi admin_user.yaml
```

```{literalinclude} /_files/centos/work/kubectl/admin_user.yaml
:language: yaml
:class: file-content
```

```sh
kubectl apply -f admin_user.yaml
```

Bind the user to the cluster-admin role:

```sh
vi admin_user_role_binding.yaml
```

:::{literalinclude} /_files/centos/work/kubectl/admin_user_role_binding.yaml
:language: yaml
:class: file-content
:::

```sh
kubectl apply -f admin_user_role_binding.yaml
```

Check the dashboard services:

```sh
kubectl get services -n kubernetes-dashboard
```

:::{literalinclude} /_files/centos/output/kubectl/get_services_dashboard.txt
:language: text
:class: cli-output
:::

Expose the `kong-proxy` service:

```sh
kubectl -n kubernetes-dashboard port-forward --address=0.0.0.0 svc/kubernetes-dashboard-kong-proxy 8443:443
```

Open the dashboard in your browser by the following URL:

```text
https://las1:8443/
```

![Dashboard Login](/_images/cluster/kubernetes/dashboard_login.png)

Generate a token for the user:

```sh
kubectl -n kubernetes-dashboard create token admin-user
```

Paste the output token into the login page.
