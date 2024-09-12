# helm

<https://helm.sh/>

The package manager for Kubernetes.

Helm is the best way to find, share, and use software built for Kubernetes.

## Install

::::{plat} linux
:vers: CentOS 8.5, Ubuntu 22.04

```sh
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod +x get_helm.sh
sudo ./get_helm.sh
```

:::{literalinclude} /_files/centos/output/get_helm.txt
:language: text
:class: cli-output
:::

```sh
helm version
```

:::{literalinclude} /_files/centos/output/helm/version.txt
:language: go
:class: cli-output
:::

::::

## Usage

Add a repository:

```sh
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
```

Show repositories:

```sh
helm repo list
```

:::{literalinclude} /_files/centos/output/helm/repo_list_2.txt
:language: text
:class: cli-output
:::

List (deployed) releases in all namespaces:

```sh
helm list -A
```

:::{literalinclude} /_files/centos/output/helm/list_a.txt
:language: text
:class: cli-output
:::

Get manifest files of a release:

```sh
helm get manifest xxxx-release
```
