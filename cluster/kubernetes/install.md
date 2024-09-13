# Install Kubernetes Packages

## By package manager

::::{plat} centos
:vers: CentOS 8.5

Add the Kubernetes repository to the system:

```sh
sudo vi /etc/yum.repos.d/kubernetes.repo
```

:::{literalinclude} /_files/centos/etc/yum.repos.d/kubernetes.repo
:language: ini
:class: file-content
:::

The `exclude` line is to prevent these packages from being changed accidentally by `dnf upgrade`.

```sh
sudo dnf install -y kubelet kubeadm kubectl --disableexcludes=kubernetes
```

Show the version:

```sh
kubeadm version -o yaml
```

:::{literalinclude} /_files/centos/output/kubeadm/version.yaml
:language: yaml
:class: cli-output
:::

::::

## Dowload kubectl manually

`kubectl` can be installed anywhere to access k8s system.

```sh
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/darwin/amd64/kubectl"
```
