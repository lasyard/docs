# helm

<https://helm.sh/>

## Prerequisites

Install `git`.

## Install

::::{plat} linux
:vers: CentOS 8.5, Ubuntu 22.04

:::{literalinclude} /_files/centos/console/helm/install.txt
:language: console
:::

Check the version:

:::{literalinclude} /_files/centos/console/helm/version.txt
:language: console
:::

::::

::::{plat} macos
:vers: macOS Monterey

:::{literalinclude} /_files/macos/console/helm/install.txt
:language: console
:::

Check the version:

:::{literalinclude} /_files/macos/console/helm/version.txt
:language: console
:::

::::

## Usage

Add a repository:

```console
$ helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
"prometheus-community" has been added to your repositories
```

Show repositories:

:::{literalinclude} /_files/centos/console/helm/repo_list_prometheus.txt
:language: console
:::

List (deployed) releases in all namespaces:

```sh
helm list -A
```

Get manifest files of a release:

```sh
helm get manifest xxxx-release
```
